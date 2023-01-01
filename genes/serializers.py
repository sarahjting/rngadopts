from colors.models import ColorPool
from colors.serializers import ColorPoolListSerializer
from genes.models import Gene, GeneLayer, GenePool
from rest_framework import serializers


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
        fields = ['id', 'image', 'type', 'color_key', 'sort']

    id = serializers.ReadOnlyField()


class GeneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gene
        fields = ['id', 'color_pool', 'name',
                  'weight', 'date_updated', 'gene_layers']

    id = serializers.ReadOnlyField()
    gene_layers = GeneLayerSerializer(read_only=True, many=True)
    color_pool = ColorPoolListSerializer(read_only=True, allow_null=True)


class GenePoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenePool
        fields = ['id', 'color_pool', 'name', 'type', 'genes',
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
            adopt_id = self.instance.adopt_id
        else:
            adopt_id = self.context.get('adopt_id', None)

        if adopt_id:
            self.fields['color_pool_id'] = serializers.PrimaryKeyRelatedField(
                source='color_pool',
                required=True,
                queryset=ColorPool.objects.filter(date_deleted=None, adopt_id=adopt_id))

    class Meta:
        model = GenePool
        fields = ['id', 'color_pool_id', 'color_pool', 'name', 'type', 'genes',
                  'genes_count', 'genes_weight_total', 'date_updated', 'adopt']

    id = serializers.ReadOnlyField()
    color_pool = ColorPoolListSerializer(read_only=True)
    genes = GeneListSerializer(read_only=True, many=True)
    adopt = serializers.SerializerMethodField(read_only=True)
    genes_count = serializers.ReadOnlyField()
    genes_weight_total = serializers.ReadOnlyField()

    def get_adopt(self, obj):
        from adopts.serializers import AdoptListSerializer
        return AdoptListSerializer(obj.adopt, read_only=True).data


class GeneSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and isinstance(self.instance, Gene):
            adopt_id = self.instance.gene_pool.adopt_id
        else:
            adopt_id = self.context.get('adopt_id', None)

        if adopt_id:
            self.fields['color_pool_id'] = serializers.PrimaryKeyRelatedField(
                source='color_pool',
                allow_null=True,
                queryset=ColorPool.objects.filter(
                    date_deleted=None, adopt_id=adopt_id),
                default=None)

    class Meta:
        model = Gene
        fields = ['id', 'color_pool_id',
                  'color_pool', 'name', 'weight', 'date_updated', 'gene_layers', 'adopt', 'gene_pool']

    id = serializers.ReadOnlyField()
    adopt = serializers.SerializerMethodField()
    gene_pool = GenePoolListSerializer(read_only=True)
    color_pool = ColorPoolListSerializer(read_only=True, allow_null=True)
    gene_layers = GeneLayerSerializer(read_only=True, many=True)

    def get_adopt(self, obj):
        from adopts.serializers import AdoptListSerializer
        return AdoptListSerializer(obj.adopt, read_only=True).data
