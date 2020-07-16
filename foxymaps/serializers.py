from rest_framework import serializers
from .models import Location

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('__all__')

class BoundingBoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'name', 'lon', 'lat', 'lon_lat', 'size_in_hectares')
