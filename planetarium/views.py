from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from django.db.models import Count, F
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from planetarium.models import AstronomyShow, ShowTheme, PlanetariumDome, ShowSession, Ticket, Reservation
from planetarium.serializers import AstronomyShowSerializer, ShowThemeSerializer, PlanetariumDomeSerializer, \
    ShowSessionSerializer, TicketSerializer, ReservationSerializer, ShowSessionListSerializer, TicketListSerializer, \
    AstronomyShowListSerializer, AstronomyShowRetrieveSerializer, ShowSessionRetrieveSerializer, \
    ReservationListSerializer
from planetarium.permissions import IsAdminAll_or_IsAuthenticatedReadOnly, IsAuthenticatedReadOnly


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer
    permission_classes = (IsAdminAll_or_IsAuthenticatedReadOnly,)

    @staticmethod
    def _params_to_int(query_string):
        return [int(str_id) for str_id in query_string.split(",")]

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer
        if self.action == "retrieve":
            return AstronomyShowRetrieveSerializer
        return AstronomyShowSerializer

    def get_queryset(self):
        queryset = self.queryset

        show_themes = self.request.query_params.get("show_themes")

        if show_themes:
            show_themes = self._params_to_int(show_themes)
            queryset = queryset.filter(show_themes__id__in=show_themes)
        if self.action in ("list", "retrieve"):
            return queryset.prefetch_related("show_themes").distinct()
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "show_themes",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by show_themes id  (/?show_themes=1,2)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of all AstronomyShows"""
        return super().list(request, *args, **kwargs)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminAll_or_IsAuthenticatedReadOnly,)


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminAll_or_IsAuthenticatedReadOnly,)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer
    permission_classes = (IsAdminAll_or_IsAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        if self.action == "retrieve":
            return ShowSessionRetrieveSerializer
        return ShowSessionSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in "retrieve":
            queryset = queryset.select_related()
        elif self.action in "list":
            queryset = (
                queryset.select_related().annotate(tickets_taken=Count("tickets"))
            )
            seats_in_planetarium_dome = F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row")
            queryset = (
                queryset.select_related().annotate(tickets_available=seats_in_planetarium_dome - Count("tickets"))
            )
        return queryset


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        return TicketSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = queryset.select_related()
        return queryset.filter(reservation__user=self.request.user)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReservationListSerializer
        return ReservationSerializer
