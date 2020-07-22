from rest_framework import serializers
from .models import Location

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('__all__')

class LocationUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'name', 'href', 'size_in_hectares_error', 'size_in_hectares_raw', 'size_in_hectares_regex', 'size_in_hectares')

# class BoundingBoxSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Location
#         fields = ('id', 'name', 'lon', 'lat', 'lon_lat', 'size_in_hectares')
