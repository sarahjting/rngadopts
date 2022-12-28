from django.db import models
from collections import deque
import json
import re


class ColorPool(models.Model):
    adopt = models.ForeignKey(
        'adopts.Adopt', on_delete=models.RESTRICT, related_name='color_pools')
    name = models.CharField(max_length=40)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(null=True)
    colors = models.TextField(default='')

    def __str__(self):
        return self.name

    def colors_json(self):
        return json.dumps(self.colors_dict())

    def colors_dict(self):
        colors = Color.from_db(self.colors)
        return [x.to_dict() for x in colors]


class Color:
    def __init__(self, name, palettes):
        assert isinstance(name, str)
        assert isinstance(palettes, list)
        for i in range(0, len(palettes)):
            assert isinstance(palettes[i], ColorPalette)

        self.name = name
        self.palettes = palettes

    def __str__(self):
        return ' '.join([self.name] + [x.__str__() for x in self.palettes])

    def from_db(data):
        colors = []
        lines = data.split('\n')
        for i in range(0, len(lines)):
            d = deque([x for x in [x.strip(' ')
                      for x in lines[i].split(' ')] if x])

            assert len(
                d) > 0 and d[0][0] != '#', 'Line %d: Missing color name' % (i + 1)

            name = d.popleft()
            palettes = []
            while len(d) >= 3:
                try:
                    palettes.append(
                        ColorPalette(d.popleft(), d.popleft(), d.popleft()))
                except AssertionError:
                    raise AssertionError(
                        'Line {}, color {}: Has invalid hex code formatting. Refer to some sample imports.'.format(name, i + 1))

            colors.append(Color(name, palettes))
        return colors

    def to_dict(self):
        return {'name': self.name, 'palettes': [x.to_dict() for x in self.palettes]}


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
