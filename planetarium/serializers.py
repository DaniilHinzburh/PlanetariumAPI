from rest_framework import serializers
from models import AstronomyShow, ShowTheme, PlanetariumDome, ShowSession, Ticket, Reservation


class PlanetariumSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    rows = serializers.IntegerField(required=True)
    seas_in_rows = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return PlanetariumDome.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.rows = validated_data.get('rows', instance.rows)
        instance.seas_in_rows = validated_data.get('seas_in_rows', instance.seas_in_rows)
        instance.save()
        return instance
