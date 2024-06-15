from django.urls import path, include
from planetarium.views import AstronomyShowViewSet, ShowThemeViewSet, PlanetariumDomeViewSet, ShowSessionViewSet, \
    TicketViewSet, ReservationViewSet
from rest_framework import routers

app_name = "planetarium"

router = routers.DefaultRouter()
router.register("astronomy_shows", AstronomyShowViewSet, basename="astronomy_shows_list")
router.register("show_themes", ShowThemeViewSet, basename="show_themes_list")
router.register("planetarium_domes", PlanetariumDomeViewSet, basename="planetarium_domes_list")
router.register("show_sessions", ShowSessionViewSet, basename="show_sessions_list")
router.register("tickets", TicketViewSet, basename="tickets_list")
router.register("reservations", ReservationViewSet, basename="reservations_list")

urlpatterns = router.urls
