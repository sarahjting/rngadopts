from adopts.models import Adopt
from adopts.serializers import AdoptSerializer
from colors.models import ColorPool
from rest_framework import serializers


class ColorPoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorPool
        fields = ['id', 'name', 'date_updated', 'colors']

    id = serializers.ReadOnlyField()


class ColorPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorPool
        fields = ['id', 'name', 'date_updated', 'colors', 'adopt']

    id = serializers.ReadOnlyField()
    adopt = AdoptSerializer(read_only=True)
