from django.db import models
from collections import deque
import json
import re
from rngadopts import mixins
from django.utils.text import slugify


class ColorQuerySet(models.QuerySet, mixins.queryset.SoftDeletes):
    pass


class ColorPool(models.Model):
    objects = ColorQuerySet.as_manager()

    adopt = models.ForeignKey(
        'adopts.Adopt', on_delete=models.RESTRICT, related_name='color_pools')
    name = models.CharField(max_length=40)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(null=True)
    colors = models.TextField(default='')

    def __str__(self):
        return self.name

    # these can probably be memoized, im lazy
    def get_color(self, color_index):
        colors = self.colors_obj

        if color_index < 0 or color_index >= len(colors):
            return None

        return self.colors_obj[color_index]

    def get_palette(self, color_index, palette_key):
        color = self.get_color(color_index)

        return None if color is None else color.get_palette(palette_key)

    def get_hex(self, color_index, palette_key, layer):
        color = self.get_color(color_index)

        return None if color is None else color.get_hex(palette_key, layer)

    @property
    def colors_obj(self):
        return Color.from_db(self.colors)

    @property
    def colors_count(self):
        return len(self.colors_dict)

    @property
    def palettes_count(self):
        colors_dict = self.colors_dict
        return 0 if len(colors_dict) == 0 else len(colors_dict[0]['palettes'])

    @property
    def colors_json(self):
        return json.dumps(self.colors_dict)

    @property
    def colors_dict(self):
        colors = Color.from_db(self.colors)
        return [x.to_dict() for x in colors]


class Color:
    def __init__(self, name, slug, palettes):
        assert isinstance(name, str)
        assert isinstance(palettes, list)
        for i in range(0, len(palettes)):
            assert isinstance(palettes[i], ColorPalette)

        self.name = name
        self.slug = slug
        self.palettes = palettes

    def __str__(self):
        return ' '.join([self.name, self.slug] + [x.__str__() for x in self.palettes])

    def get_palette(self, palette_key):
        if palette_key < 0 or palette_key >= len(self.palettes):
            return None

        return self.palettes[palette_key]

    def get_hex(self, palette_key, layer):
        palette = self.get_palette(palette_key)

        if palette is None or layer not in ["base", "shading", "highlight"]:
            return None

        return getattr(palette, layer)

    def from_db(data):
        colors = []
        lines = data.split('\n')
        for i in range(0, len(lines)):
            d = deque([x for x in [x.strip()
                      for x in lines[i].split()] if x])

            assert len(
                d) > 0 and d[0][0] != '#', 'Line %d: Missing color name' % (i + 1)

            name = d.popleft()
            slug = d.popleft() if len(d) > 0 and d[0][0] != '#' else slugify(
                name).replace("-", "").replace("_", "")
            palettes = []
            while len(d) >= 3:
                try:
                    palettes.append(
                        ColorPalette(d.popleft(), d.popleft(), d.popleft()))
                except AssertionError:
                    raise AssertionError(
                        'Line {}, color {}: Has invalid hex code formatting. Refer to some sample imports.'.format(name, i + 1))

            colors.append(Color(name, slug, palettes))
        return colors

    def to_dict(self):
        return {'name': self.name, 'slug': self.slug, 'palettes': [x.to_dict() for x in self.palettes]}


class ColorPalette:
    def __init__(self, base, shading, highlight):
        assert re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', base)
        assert re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', shading)
        assert re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', highlight)

        self.base = base
        self.shading = shading
        self.highlight = highlight

    def __str__(self):
        return ' '.join([self.base, self.shading, self.highlight])

    def to_dict(self):
        return {'base': self.base, 'shading': self.shading, 'highlight': self.highlight}
