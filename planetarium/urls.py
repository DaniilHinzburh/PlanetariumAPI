from django.urls import path, include
from planetarium.views import PlanetariumDomeViewSet
from rest_framework import routers

app_name = "planetarium"

router = routers.DefaultRouter()
router.register("planetarium_domes", PlanetariumDomeViewSet, basename="planetarium_domes_list")

urlpatterns = router.urls
