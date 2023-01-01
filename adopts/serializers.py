from adopts.models import Adopt, AdoptLayer
from genes.models import GenePool
from genes.serializers import GenePoolListSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator


class AdoptListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopt
        fields = ['id', 'name', 'short_name', 'logs_count',
                  'current_display_id', 'date_updated']
    id = serializers.ReadOnlyField()
    logs_count = serializers.ReadOnlyField()
    current_display_id = serializers.ReadOnlyField()


class AdoptLayerSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and isinstance(self.instance, AdoptLayer):
            adopt_id = self.instance.adopt_id
        else:
            adopt_id = self.context.get('adopt_id', None)

        if adopt_id:
            self.fields['gene_pool_id'] = serializers.PrimaryKeyRelatedField(
                source='gene_pool',
                queryset=GenePool.objects.filter(
                    date_deleted=None, adopt_id=adopt_id),
                default=None,
                required=False)

    class Meta:
        model = AdoptLayer
        fields = ['id', 'image', 'type', 'gene_pool', 'sort']

    id = serializers.ReadOnlyField()
    gene_pool = GenePoolListSerializer(read_only=True)
    sort = serializers.IntegerField(default=0)


class AdoptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopt
        fields = ['id', 'name', 'short_name', 'width', 'height', 'logs_count', 'current_display_id',
                  'layers_count', 'colors_count', 'genes_count', 'date_updated', 'adopt_layers', 'gen_caption']
    id = serializers.ReadOnlyField()
    short_name = serializers.SlugField(
        validators=[UniqueValidator(queryset=Adopt.objects), RegexValidator(
            '^[A-Za-z0-9]+$',
            message="Must be alphanumeric"
        )])
    logs_count = serializers.ReadOnlyField()
    layers_count = serializers.ReadOnlyField()
    genes_count = serializers.ReadOnlyField()
    colors_count = serializers.ReadOnlyField()
    adopt_layers = AdoptLayerSerializer(read_only=True, many=True)
    gen_caption = serializers.CharField(allow_blank=True)
