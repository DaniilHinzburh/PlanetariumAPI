from planetarium.models import PlanetariumDome
from planetarium.serializers import PlanetariumSerializer
from rest_framework import generics


class PlanetariumDomeList(generics.ListCreateAPIView):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumSerializer


class PlanetariumDomeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumSerializer
