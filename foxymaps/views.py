# from rest_framework.views import APIView # get the APIView class from DRF
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.response import Response # get the Response class from DRF

from .models import Location
from .serializers import LocationSerializer, LocationUpdateSerializer, LocationSpeedSerializer

class LocationList(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetail(RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

# class LocationSpeedList(ListCreateAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationSpeedSerializer

class LocationFilterList(ListCreateAPIView):
    """ Filter by the field needed.  Currently set to size_in_hectares_error """
    queryset = Location.objects.all().filter(size_in_hectares_error=True)
    serializer_class = LocationUpdateSerializer
