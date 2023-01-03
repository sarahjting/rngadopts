from colors.models import ColorPool
from colors.serializers import ColorPoolListSerializer
from genes.models import Gene, GeneLayer, GenePool
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.validators import RegexValidator


class GeneLayerSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        adopt_id = self.context.get('adopt_id', None)

        if adopt_id:
            self.fields['gene_id'] = serializers.PrimaryKeyRelatedField(
                required=True,
                source='gene',
                queryset=Gene.objects.filter(date_deleted=None, gene_pool__adopt_id=adopt_id))

    class Meta:
        model = GeneLayer
        fields = ['id', 'image', 'type',
                  'color_key', 'required_gene_id', 'sort']

    id = serializers.ReadOnlyField()
    required_gene_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        source='required_gene',
        queryset=Gene.objects.filter(date_deleted=None))


class GeneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gene
        fields = ['id', 'color_pool', 'name', 'slug',
                  'weight', 'date_updated', 'gene_layers']

    id = serializers.ReadOnlyField()
    gene_layers = GeneLayerSerializer(read_only=True, many=True)
    color_pool = ColorPoolListSerializer(read_only=True, allow_null=True)


class GenePoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenePool
        fields = ['id', 'color_pool', 'name', 'slug', 'type', 'genes',
                  'genes_count', 'genes_weight_total', 'date_updated']

    id = serializers.ReadOnlyField()
    genes_count = serializers.ReadOnlyField()
    genes_weight_total = serializers.ReadOnlyField()
    color_pool = ColorPoolListSerializer(read_only=True)
    genes = GeneListSerializer(read_only=True, many=True)


class GenePoolSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # if a gene pool was passed in, the possible color pools are all color pools belonging to the same adopt
        # if no gene pool was passed in, we're currently creating; an adopt_id should have been passed in with the context
        # it's possible for this to be a QuerySet
        if self.instance and isinstance(self.instance, GenePool):
            adopt = self.instance.adopt
        else:
            adopt = self.context.get('adopt', None)

        if adopt:
            self.fields['color_pool_id'] = serializers.PrimaryKeyRelatedField(
                source='color_pool',
                required=True,
                queryset=ColorPool.objects.filter(date_deleted=None, adopt_id=adopt.id))

    class Meta:
        model = GenePool
        fields = ['id', 'color_pool_id', 'color_pool', 'slug', 'name', 'type', 'genes',
                  'genes_count', 'genes_weight_total', 'date_updated', 'adopt']

    id = serializers.ReadOnlyField()
    color_pool = ColorPoolListSerializer(read_only=True)
    genes = GeneListSerializer(read_only=True, many=True)
    adopt = serializers.SerializerMethodField(read_only=True)
    genes_count = serializers.ReadOnlyField()
    genes_weight_total = serializers.ReadOnlyField()
    slug = serializers.SlugField(
        validators=[
            RegexValidator(
                '^[A-Za-z0-9]+$',
                message="Must be alphanumeric"
            ),
        ])

    def validate(self, data):
        def validate_slug(slug, adopt):
            if GenePool.objects.filter(adopt_id=adopt.id, slug=slug).exclude(id=self.instance.id if self.instance else None).active().exists():
                raise serializers.ValidationError(
                    {"slug": "This slug is in use."})

        # update
        if self.instance and isinstance(self.instance, GenePool):
            validate_slug(data["slug"], self.instance.adopt)

        # create
        else:
            validate_slug(data["slug"], self.context.get('adopt'))

        return data

    def get_adopt(self, obj):
        from adopts.serializers import AdoptListSerializer
        return AdoptListSerializer(obj.adopt, read_only=True).data


class GeneSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and isinstance(self.instance, Gene):
            adopt_id = self.instance.gene_pool.adopt_id
        else:
            adopt_id = self.context.get('adopt', None).id

        if adopt_id:
            self.fields['color_pool_id'] = serializers.PrimaryKeyRelatedField(
                source='color_pool',
                allow_null=True,
                queryset=ColorPool.objects.filter(
                    date_deleted=None, adopt_id=adopt_id),
                default=None)

    class Meta:
        model = Gene
        fields = ['id', 'has_color', 'color_pool_id', 'color_pool', 'name', 'slug',
                  'weight', 'date_updated', 'gene_layers', 'adopt', 'gene_pool']

    id = serializers.ReadOnlyField()
    adopt = serializers.SerializerMethodField()
    gene_pool = GenePoolListSerializer(read_only=True)
    color_pool = ColorPoolListSerializer(read_only=True, allow_null=True)
    gene_layers = GeneLayerSerializer(read_only=True, many=True)
    slug = serializers.SlugField(
        validators=[
            RegexValidator(
                '^[A-Za-z0-9]+$',
                message="Must be alphanumeric"
            ),
        ])

    def validate(self, data):
        def validate_slug(slug, gene_pool):
            if Gene.objects.filter(gene_pool_id=gene_pool.id, slug=slug).exclude(id=self.instance.id if self.instance else None).active().exists():
                raise serializers.ValidationError(
                    {"slug": "This slug is in use."})

        # update
        if self.instance and isinstance(self.instance, Gene):
            validate_slug(data["slug"], self.instance.gene_pool)

        # create
        else:
            validate_slug(data["slug"], self.context.get('gene_pool'))

        return data

    def get_adopt(self, obj):
        from adopts.serializers import AdoptListSerializer
        return AdoptListSerializer(obj.adopt, read_only=True).data
