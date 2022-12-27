from colors.models import ColorPool
from rest_framework import serializers


class ColorPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorPool
        fields = ['id', 'name', 'date_updated', 'colors']

    id = serializers.ReadOnlyField()
