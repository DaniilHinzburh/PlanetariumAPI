from django.urls import path, include
from planetarium.views import AstronomyShowViewSet, ShowThemeViewSet, PlanetariumDomeViewSet, ShowSessionViewSet, \
    TicketViewSet, ReservationViewSet
from rest_framework import routers

app_name = "planetarium"

router = routers.DefaultRouter()
router.register("astronomy_shows", AstronomyShowViewSet)
router.register("show_themes", ShowThemeViewSet)
router.register("planetarium_domes", PlanetariumDomeViewSet)
router.register("show_sessions", ShowSessionViewSet)
router.register("tickets", TicketViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = router.urls
