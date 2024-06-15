from rest_framework import serializers
from planetarium.models import AstronomyShow, ShowTheme, PlanetariumDome, ShowSession, Ticket, Reservation


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_themes")


class AstronomyShowListSerializer(AstronomyShowSerializer):
    show_themes = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")


class AstronomyShowRetrieveSerializer(AstronomyShowSerializer):
    show_themes = ShowThemeSerializer(many=True)


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "category")


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionListSerializer(serializers.ModelSerializer):
    astronomy_show = AstronomyShowListSerializer()
    planetarium_dome_name = serializers.CharField(source="planetarium_dome.name")
    planetarium_dome_num_seats = serializers.SerializerMethodField()
    planetarium_dome_category = serializers.CharField(source="planetarium_dome.category")

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "show_time", "planetarium_dome_name", "planetarium_dome_num_seats",
                  "planetarium_dome_category")

    def get_planetarium_dome_num_seats(self, obj):
        return obj.planetarium_dome.rows * obj.planetarium_dome.seats_in_row


class ShowSessionRetrieveSerializer(ShowSessionSerializer):
    planetarium_dome = PlanetariumDomeSerializer(many=False, read_only=True)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session", "reservation")


class TicketListSerializer(TicketSerializer):
    show_session = ShowSessionListSerializer()


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")
