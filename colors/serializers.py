from colors.models import ColorPool, Color
from rest_framework import serializers
from rest_framework.serializers import ValidationError


class ColorsField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            colors = Color.from_db(data)
        except AssertionError as e:
            raise ValidationError(e)

        return '\n'.join([x.__str__() for x in colors])


class ColorPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorPool
        fields = ['id', 'name', 'date_updated', 'colors', 'colors_json']

    id = serializers.ReadOnlyField()
    colors = ColorsField()
    colors_json = serializers.ReadOnlyField()
