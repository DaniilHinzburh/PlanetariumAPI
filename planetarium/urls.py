from django.urls import path, include
from planetarium.views import PlanetariumDomeList, PlanetariumDomeDetail

app_name = "planetarium"

urlpatterns = [
    path("planetarium_domes/", PlanetariumDomeList.as_view(), name="planetarium_domes_list"),
    path("planetarium_domes/<int:pk>/", PlanetariumDomeDetail.as_view(), name="planetarium_dome_detail")
]
