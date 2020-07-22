# from rest_framework.views import APIView # get the APIView class from DRF
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.response import Response # get the Response class from DRF

from .models import Location
from .serializers import LocationSerializer, LocationUpdateSerializer

# def handle(self, *_args, **_options):
#     LocationHectareList.get(self, *_args, **_options)

class LocationList(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationHectareList(ListCreateAPIView):
    queryset = Location.objects.all().filter(size_in_hectares_error=True)
    serializer_class = LocationUpdateSerializer
    # response = serializer_class.data
    # print(response)

class LocationDetail(RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all().filter(size_in_hectares_error=True)
    serializer_class = LocationUpdateSerializer
