import json
import random
from PIL import Image
from django.db.models import Prefetch
from genes.models import Gene
from django.utils.text import slugify


class AdoptGeneratorImage:
    """
    TODO: Write snapshot tests
    """

    def __init__(self, gen):
        self.gen = gen
        self.width = self.gen.adopt.width
        self.height = self.gen.adopt.height
        self.pil = Image.new(
            "RGBA", (self.width, self.height), (255, 255, 255, 0))
        self.generate()

    def generate(self):
        adopt_layers = list(self.gen.adopt.adopt_layers.order_by("sort").all())

        # build base layer
        base_pil = self._build_light_level(adopt_layers, "base")

        # build shading layer
        shading_pil = self._build_light_level(adopt_layers, "shading")
        shading_mask = self._build_light_level_mask(adopt_layers, "shading")
        shading_pil.putalpha(shading_mask)
        base_pil.alpha_composite(shading_pil)

        # build highlight layer
        highlight_pil = self._build_light_level(adopt_layers, "highlight")
        highlight_mask = self._build_light_level_mask(
            adopt_layers, "highlight")
        highlight_pil.putalpha(highlight_mask)
        base_pil.alpha_composite(highlight_pil)

        self.pil = base_pil

    def _find_gene(self, gene_id):
        """
        If gene exists in the gen, return the gene color. If not, return None.
        """
        res = [gc for gc in self.gen.gene_colors if gc["gene"].id == gene_id]
        return res[0] if len(res) > 0 else None

    def _find_gene_pool(self, gene_pool_id):
        """
        Return a list with all gene colors belonging to the gene pool.
        """
        return [gc for gc in self.gen.gene_colors if gc["gene"].gene_pool_id == gene_pool_id]

    def _build_light_level(self, adopt_layers, light_level):
        """
        Generates either a base, shading, or highlight image and returns a PIL Image
        """

        def draw_gene_color_layer(pil, gene_color, gene_layer):
            gene_type = gene_layer.type.split("_")[0]
            if gene_type == "static":
                self._draw_file(pil, gene_layer.image.path)
            elif gene_type == "color":
                color = gene_color["color"]

                # if there's a required gene, we can assume it exists; take color from there if possible
                if gene_layer.required_gene_id:
                    required_gc = self._find_gene(gene_layer.required_gene_id)
                    if required_gc:
                        color = required_gc["color"]
                    else:
                        return

                if gene_layer.required_gene_pool_id:
                    required_gcs = self._find_gene_pool(
                        gene_layer.required_gene_pool_id)
                    if len(required_gcs) > 0:
                        color = required_gcs[0]["color"]
                    else:
                        return

                if color == None:
                    return

                self._draw_file_color(pil, gene_layer.image.path, color.get_hex(
                    gene_layer.color_key - 1, light_level))

        def draw_adopt_layer(pil, adopt_layer):
            if adopt_layer.type == "static":
                self._draw_file(pil, adopt_layer.image.path)

        return self._draw_adopt_layers(self._new_pil(), adopt_layers, draw_adopt_layer=draw_adopt_layer, draw_gene_color_layer=draw_gene_color_layer)

    def _build_light_level_mask(self, adopt_layers, light_level):
        """
        Generates either a shading mask or a highlight mask and returns a PIL Image
        """

        def draw_gene_color_layer(pil, gene_color, gene_layer):
            gene_type, gene_depth = gene_layer.type.split("_")
            if gene_type == light_level:
                self._draw_file_color(pil, gene_layer.image.path, "#FFFFFF")
            elif gene_type == "color" and gene_depth != "on":
                self._draw_file_color(
                    pil, gene_layer.image.path, "#000000")

        def draw_adopt_layer(pil, adopt_layer):
            if adopt_layer.type == light_level:
                self._draw_file_color(pil, adopt_layer.image.path, "#FFFFFF")

        return self._draw_adopt_layers(self._new_pil("#000000", mode="L"), adopt_layers, draw_adopt_layer=draw_adopt_layer, draw_gene_color_layer=draw_gene_color_layer)

    def _draw_adopt_layers(self, pil, adopt_layers, draw_adopt_layer, draw_gene_color_layer):
        """
        Iterates through all adopt layers and runs the provided function on each adopt layer / gc layer 
        """
        for depth in ["under", "on", "over"]:
            for adopt_layer in adopt_layers:
                if adopt_layer.type != "gene" and depth == "over":
                    # adopt layers only get drawn once on the "over" depth
                    draw_adopt_layer(pil, adopt_layer)
                    continue

                # check if we have this gene pool assigned, otherwise we skip
                # it's completely possible to have multiple genes here (for multi gene pools)
                gene_colors = [x for x in self.gen.gene_colors
                               if x["gene"].gene_pool_id == adopt_layer.gene_pool_id]

                if len(gene_colors) == 0:
                    continue

                for gene_color in gene_colors:
                    for gene_layer in reversed(gene_color["gene"].gene_layers.all()):
                        # check for required gene
                        if gene_layer.required_gene_id and not self._find_gene(gene_layer.required_gene_id):
                            continue

                        # check for required gene_pool
                        if gene_layer.required_gene_pool_id and len(self._find_gene_pool(gene_layer.required_gene_pool_id)) == 0:
                            continue

                        # check if we're at the correct depth to draw this
                        gene_type, gene_depth = gene_layer.type.split("_")
                        if gene_depth != depth:
                            continue

                        # draw
                        draw_gene_color_layer(pil, gene_color, gene_layer)
        return pil

    def _new_pil(self, hex=(255, 255, 255, 0), mode="RGBA"):
        return Image.new(mode, (self.width, self.height), hex)

    def _file_pil(self, path):
        try:
            new_image = Image.open(path, 'r')

            # if the image is the wrong width or height, we crop it then paste it on a correctly sized transparent image
            if new_image.width != self.width or new_image.height != self.height:
                base_image = self._new_pil()
                new_image = new_image.crop((0, 0, self.width, self.height))
                self._draw_file(base_image, new_image)
                return base_image

            return new_image
        except AttributeError:
            # this occurs if there is no image found at the path location
            return self._new_pil()

    def _draw_file(self, pil, path):
        pil.alpha_composite(self._file_pil(path))

    def _draw_file_color(self, pil, path, hex):
        pil.paste(self._new_pil(hex), self._file_pil(path))

    def to_pil(self):
        return self.pil


class AdoptGenerator:
    def __init__(self, adopt):
        self.adopt = adopt
        self.gene_colors = []  # [{gene color_pool color}]

    def randomize(self):
        genes = AdoptGeneratorGenePicker(self.adopt).pick()

        gene_colors = []
        for gene in genes:
            color_pool = gene.color_pool or gene.gene_pool.color_pool
            gene_colors.append({
                "gene": gene,
                "color_pool": color_pool,
                "color": color_pool.get_color(random.randint(0, color_pool.colors_count - 1)),
            })

        self.gene_colors = gene_colors
        return self

    def to_dict(self):
        # this is for log and display
        # TODO: save a historical version of the color pool on every update and have logs point towards the version ID
        return {
            "adopt_id": self.adopt.id,
            "gene_colors": [{
                "gene": {"id": gene_color["gene"].id, "name": gene_color["gene"].name, "gene_pool_id": gene_color["gene"].gene_pool_id},
                "color": {"name": gene_color["color"].name, "slug": gene_color["color"].slug, "color_pool_id": gene_color["color_pool"].id} if gene_color["color"] else None,
            } for gene_color in self.gene_colors]
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def clean_slugify(self, str):
        # we can't have these in the url strings
        return slugify(str).replace("-", "").replace("_", "")

    def to_data_string(self, display_id=False):
        return "-".join(
            [self.clean_slugify(self.adopt.short_name)] +
            ([] if display_id == False else [str(display_id) if not isinstance(
                display_id, bool) else str(self.adopt.current_display_id)]) +
            sorted([
                "_".join([
                    gc['gene'].gene_pool.slug,
                    gc['gene'].slug,
                ] + ([gc['color'].slug] if gc['gene'].get_has_color() else [])) for gc in self.gene_colors
            ]))

    def from_data_string(self, data_string):
        raw_gene_colors = [x.split("_") for x in data_string.split("-")]
        gene_pools = AdoptGeneratorGenePicker(self.adopt).gene_pools

        self.gene_colors = []
        for raw_gc in raw_gene_colors:
            try:
                gene_pool, = [x for x in gene_pools if x.slug == raw_gc[0]]
                gene, = [x for x in gene_pool.genes.all() if x.slug ==
                         raw_gc[1]]
                color_pool = gene.color_pool or gene_pool.color_pool
                color, = [x for x in color_pool.colors_obj if x.slug ==
                          raw_gc[2]] if len(raw_gc) == 3 else (None,)
                self.gene_colors.append(
                    {"gene": gene, "color_pool": color_pool, "color": color})
            except ValueError:
                pass

        return self

    def __str__(self):
        return f"{self.adopt.name}: " + ", ".join([f"{gene_color['gene'].name} ({gene_color['color'].name})" for gene_color in self.gene_colors])


# i wonder if python prefers this to be a function or class? PHP likes classes for easier composition
# i brought this into the adopts domain as a class bc it relies on an eager load on the adopt model and i want to keep the code together
class AdoptGeneratorGenePicker:
    def __init__(self, adopt):
        self.adopt = adopt
        self.gene_pools = list(self.adopt.gene_pools.prefetch_related(
            Prefetch(
                "genes",
                queryset=Gene.objects.active().order_by("name"),
            )
        ).prefetch_related("color_pool").prefetch_related("genes__color_pool").prefetch_related("genes__gene_layers").all())

    def pick(self):
        genes = []

        for gene_pool in self.gene_pools:
            genes.extend(self.pick_from_pool(gene_pool))

        return genes

    def pick_from_pool(self, gene_pool):
        all_genes = gene_pool.genes.all()
        if len(all_genes) == 0:
            return []

        selected_genes = []

        if gene_pool.type == "multi":
            for gene in all_genes:
                if random.randint(1, 100) <= gene.weight:
                    selected_genes.append(gene)
        else:
            i = 0
            pool_weight = sum([x.weight for x in all_genes])
            offset = random.randint(1, pool_weight)
            while True:
                offset -= all_genes[i].weight
                if offset <= 0 or i >= len(all_genes):
                    selected_genes.append(all_genes[i])
                    break
                i += 1

        return selected_genes
