from planetarium.models import PlanetariumDome
from planetarium.serializers import PlanetariumSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404


class PlanetariumDomeList(APIView):
    def get(self, request) -> Response:
        planetarium_domes = PlanetariumDome.objects.all()
        serializer = PlanetariumSerializer(planetarium_domes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request) -> Response:
        serializer = PlanetariumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanetariumDomeDetail(APIView):
    def get_object(self, pk) -> PlanetariumDome:
        return get_object_or_404(PlanetariumDome, pk=pk)

    def get(self, request, pk) -> Response:
        serializer = PlanetariumSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk) -> Response:
        serializer = PlanetariumSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(self.get_object(pk), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk) -> Response:
        serializer = PlanetariumSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(self.get_object(pk), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk) -> Response:
        planetarium = self.get_object(pk)
        planetarium.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)