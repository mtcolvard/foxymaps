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

class LocationSpeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id',
        'name',
        'type_of_site',
        'listed_structures',
        'open_to_public',
        'opening_times',
        'facilities',
        'lon_lat',
        'lon',
        'lat',
        'on_eh_national_register',
        'eh_grade',
        'in_conservation_area',
        'tree_preservation_order',
        'nature_conservation_area',
        'green_belt',
        'metropolitan_open_land',
        'size_in_hectares',
        )


# class BoundingBoxSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Location
#         fields = ('id', 'name', 'lon', 'lat', 'lon_lat', 'size_in_hectares')
