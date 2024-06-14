from planetarium.models import PlanetariumDome
from planetarium.serializers import PlanetariumSerializer
from rest_framework import viewsets


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumSerializer
