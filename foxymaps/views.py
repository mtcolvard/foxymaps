# from rest_framework.views import APIView # get the APIView class from DRF
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.response import Response # get the Response class from DRF

from .models import Location
from .serializers import LocationSerializer

class LocationList(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetail(RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
