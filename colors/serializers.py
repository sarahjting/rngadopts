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


class ColorPoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorPool
        fields = ['id', 'name', 'date_updated', 'colors', 'colors_dict']

    id = serializers.ReadOnlyField()
    colors = ColorsField()
    colors_dict = serializers.ReadOnlyField()


class ColorPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorPool
        fields = ['id', 'name', 'date_updated',
                  'colors', 'colors_dict', 'adopt']

    id = serializers.ReadOnlyField()
    colors = ColorsField()
    colors_dict = serializers.ReadOnlyField()
    adopt = serializers.SerializerMethodField()

    def get_adopt(self, obj):
        from adopts.serializers import AdoptListSerializer
        return AdoptListSerializer(obj.adopt, read_only=True).data
