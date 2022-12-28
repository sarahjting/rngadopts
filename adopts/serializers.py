from adopts.models import Adopt, AdoptLayer
from colors.models import ColorPool
from colors.serializers import ColorPoolSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class AdoptListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopt
        fields = ['id', 'name', 'short_name',
                  'logs_count', 'layers_count', 'genes_count', 'date_updated']
    id = serializers.ReadOnlyField()
    logs_count = serializers.ReadOnlyField()
    layers_count = serializers.ReadOnlyField()
    genes_count = serializers.ReadOnlyField()


class AdoptLayerSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and isinstance(self.instance, AdoptLayer):
            adopt_id = self.instance.adopt_id
        else:
            adopt_id = self.context.get('adopt_id', None)

        if adopt_id:
            self.fields['color_pool_id'] = serializers.PrimaryKeyRelatedField(
                source='color_pool',
                queryset=ColorPool.objects.filter(
                    date_deleted=None, adopt_id=adopt_id),
                default=None)

    class Meta:
        model = AdoptLayer
        fields = ['id', 'image', 'type', 'color_pool', 'sort']

    id = serializers.ReadOnlyField()
    color_pool = ColorPoolSerializer(read_only=True)
    sort = serializers.IntegerField(default=0)


class AdoptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopt
        fields = ['id', 'name', 'short_name',
                  'logs_count', 'layers_count', 'genes_count', 'date_updated', 'adopt_layers']
    id = serializers.ReadOnlyField()
    short_name = serializers.SlugField(
        validators=[UniqueValidator(queryset=Adopt.objects)])
    logs_count = serializers.ReadOnlyField()
    layers_count = serializers.ReadOnlyField()
    genes_count = serializers.ReadOnlyField()
    adopt_layers = AdoptLayerSerializer(read_only=True, many=True)
