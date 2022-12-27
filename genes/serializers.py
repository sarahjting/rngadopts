from adopts.serializers import AdoptSerializer
from colors.models import ColorPool
from colors.serializers import ColorPoolSerializer
from genes.models import Gene, GenePool
from rest_framework import serializers


class GenePoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenePool
        fields = ['id', 'color_pool', 'name', 'type',
                  'genes_count', 'genes_weight_total', 'date_updated']

    id = serializers.ReadOnlyField()
    genes_count = serializers.ReadOnlyField()
    genes_weight_total = serializers.ReadOnlyField()
    color_pool = ColorPoolSerializer(read_only=True)


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
        fields = ['id', 'adopt', 'color_pool_id', 'color_pool', 'name', 'type',
                  'genes_count', 'genes_weight_total', 'date_updated']

    id = serializers.ReadOnlyField()
    adopt = AdoptSerializer(read_only=True)
    color_pool = ColorPoolSerializer(read_only=True)
    genes_count = serializers.ReadOnlyField()
    genes_weight_total = serializers.ReadOnlyField()


class GeneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gene
        fields = ['id', 'color_pool', 'name', 'weight', 'date_updated']

    id = serializers.ReadOnlyField()
    color_pool = ColorPoolSerializer(read_only=True, allow_null=True)


class GeneSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # if a gene was passed in, the possible color pools are all color pools belonging to the same adopt
        # if no gene was passed in, we're currently creating; an adopt_id should have been passed in with the context
        if self.instance and isinstance(self.instance, Gene):
            adopt_id = self.instance.gene_pool.adopt_id
        else:
            adopt_id = self.context.get('adopt_id', None)

        if adopt_id:
            self.fields['color_pool_id'] = serializers.PrimaryKeyRelatedField(
                source='color_pool',
                allow_null=True,
                queryset=ColorPool.objects.filter(date_deleted=None, adopt_id=adopt_id))

    class Meta:
        model = Gene
        fields = ['id', 'gene_pool', 'color_pool_id',
                  'color_pool', 'name', 'weight', 'date_updated']

    id = serializers.ReadOnlyField()
    gene_pool = GenePoolSerializer(read_only=True)
    color_pool = ColorPoolSerializer(read_only=True, allow_null=True)
