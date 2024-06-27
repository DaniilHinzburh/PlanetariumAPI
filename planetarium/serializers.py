from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from planetarium.models import AstronomyShow, ShowTheme, PlanetariumDome, ShowSession, Ticket, Reservation


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_themes", "image")


class AstronomyShowListSerializer(AstronomyShowSerializer):
    show_themes = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")


class AstronomyShowRetrieveSerializer(AstronomyShowSerializer):
    show_themes = ShowThemeSerializer(many=True)


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "category")


class PlanetariumDomeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name",)


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionListSerializer(serializers.ModelSerializer):
    astronomy_show = AstronomyShowListSerializer()
    planetarium_dome_name = serializers.CharField(source="planetarium_dome.name")
    planetarium_dome_num_seats = serializers.SerializerMethodField()
    planetarium_dome_category = serializers.CharField(source="planetarium_dome.category")

    tickets_taken = serializers.IntegerField(read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "show_time", "planetarium_dome_name", "planetarium_dome_num_seats",
                  "planetarium_dome_category", "tickets_taken", "tickets_available")

    def get_planetarium_dome_num_seats(self, obj):
        return obj.planetarium_dome.rows * obj.planetarium_dome.seats_in_row


class ShowSessionRetrieveSerializer(ShowSessionSerializer):
    planetarium_dome = PlanetariumDomeShortSerializer(many=False, read_only=True)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session", "reservation")

    def validate(self, attrs):
        Ticket.validate_row(
            attrs["row"],
            attrs["show_session"].planetarium_dome.rows,
            serializers.ValidationError
        )
        Ticket.validate_seat(
            attrs["seat"],
            attrs["show_session"].planetarium_dome.seats_in_row,
            serializers.ValidationError
        )
        return attrs


class TicketListSerializer(TicketSerializer):
    show_session = ShowSessionRetrieveSerializer(read_only=True)


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
