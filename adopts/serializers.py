from adopts.models import Adopt
from rest_framework import serializers


class AdoptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopt
        fields = ['id', 'name', 'short_name', 'count', 'date_updated']
    id = serializers.ReadOnlyField()
    count = serializers.ReadOnlyField()
