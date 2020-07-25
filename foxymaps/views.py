import math

# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from django.http import Http404
# from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .models import Location
from .serializers import LocationSerializer, LocationUpdateSerializer, LocationSpeedSerializer, BoundingBoxSerializer

from mapbox import Geocoder
from .mapboxDirectionsAPI import DirectionsCalculations
from .distanceAndBearingCalcs import DistanceAndBearing
from .homingAlgo import run_homing_algo

class LocationList(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetail(RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationSpeedList(ListCreateAPIView):
    queryset = Location.objects.filter(size_in_hectares__gte=1).filter(open_to_public="Yes").exclude(green_belt="Yes")
    # query = Location.objects.exclude(size_in_hectares='Partially')
    # queryset = query.exclude(size_in_hectares='Yes')
    print(len(queryset))
    serializer_class = LocationSpeedSerializer

class LocationFilterList(ListCreateAPIView):
    """ Filter by the field needed.  Currently set to size_in_hectares_error """
    queryset = Location.objects.all().filter(size_in_hectares_error=True)
    serializer_class = LocationUpdateSerializer



class MapGeocoderView(APIView):
    def get(self, _request, searchQuery, bbox=None, country='ISO 3166-2:GB'):
        geocoder = Geocoder(name='mapbox.places', access_token='pk.eyJ1IjoibXRjb2x2YXJkIiwiYSI6ImNrZDIycDBuaTAyYjQyeG55azNwYzd0ZjMifQ.yYcTjTmpZ89j4vMWS8VdrA')
        response = geocoder.forward(searchQuery, bbox, country)
        data = response.json()
        print(data)
        return Response(response.json())

class RouteThenBoundingBox(APIView):
    def calculate_parks_within_perp_distance(self, parks_dict, orientation, journey_leg, best_fit, rambling_tolerance):
        parks_within_perp_distance = {
        k:v for (k, v) in parks_dict.items() if
            # select only parks within ± 45 degrees of inital bearing towards destination
            v['crowflys_distance_and_bearing'][orientation][1] < (best_fit[1] + math.pi/4) and
            v['crowflys_distance_and_bearing'][orientation][1] > (best_fit[1] - math.pi/4) and
            # select only parks within the radius from origin to destination
            v['crowflys_distance_and_bearing'][orientation][0] < best_fit[0] and
            # select parks within user's tolerance for rambling
            v['distance_from_bestfit_line'][journey_leg] <= rambling_tolerance and
            v['distance_from_bestfit_line'][journey_leg] >= 0}
        return parks_within_perp_distance

    def get(self, _request, currentWaypoint, destination, ramblingTolerance):
        rambling_tolerance = int(ramblingTolerance)
        current_waypoint_lon_lat = [float(x) for x in currentWaypoint.split(',')]
        destination_lon_lat = [float(x) for x in destination.split(',')]
        best_fit_origin_to_destination = DistanceAndBearing.crowflys_bearing(self, current_waypoint_lon_lat, destination_lon_lat)

        # queryset = Location.objects.all()
        queryset = Location.objects.filter(open_to_public='Yes')
        serializer = LocationSpeedSerializer(queryset, many=True)
        response_data = serializer.data

        parks_dict = {}
        for park in response_data:
            lon_lat = [park['lon'], park['lat']]
            crowflys_distance_and_bearing = DistanceAndBearing.crowflys_bearing(self, current_waypoint_lon_lat, lon_lat)
            size_in_hectares = park['size_in_hectares']
            try:
                size_in_hectares_float = float(size_in_hectares)
            except (TypeError, ValueError):
                size_in_hectares_float = 0.0

            parks_dict[park['id']] = {
            'id':park['id'],
            'name':park['name'],
            'lon_lat': lon_lat,
            'crowflys_distance_and_bearing': {'from_origin': crowflys_distance_and_bearing},
            'distance_from_bestfit_line': {'origin_to_destination': DistanceAndBearing.perpendicular_distance_from_bestfit_line(self, best_fit_origin_to_destination, crowflys_distance_and_bearing)},
            'size_in_hectares': size_in_hectares_float}

        parks_within_perp_distance = self.calculate_parks_within_perp_distance(parks_dict, 'from_origin', 'origin_to_destination', best_fit_origin_to_destination, rambling_tolerance)

        largestPark = parks_within_perp_distance[max(parks_within_perp_distance, key=lambda v: parks_within_perp_distance[v]['size_in_hectares'])]

        if len(parks_within_perp_distance) > 23:
            waypoints_sorted_by_acreage = sorted(parks_within_perp_distance.keys(), key=lambda y: (parks_within_perp_distance[y]['size_in_hectares']))
            print(waypoints_sorted_by_acreage)

            waypoints_sliced_by_acreage = waypoints_sorted_by_acreage[-23:]
            print(waypoints_sliced_by_acreage)

            total_waypoints_sorted_by_acreage = {k:v for k, v in parks_within_perp_distance.items() if k in waypoints_sliced_by_acreage}
            print(total_waypoints_sorted_by_acreage)
            total_waypoints_dict = {'origin': {'lon_lat': current_waypoint_lon_lat, 'crowflys_distance_and_bearing': {'from_origin': (0, 0)}}, **total_waypoints_sorted_by_acreage, 'destination': {'lon_lat': destination_lon_lat, 'crowflys_distance_and_bearing': {'from_origin': best_fit_origin_to_destination}}}
        else:
            total_waypoints_dict = {'origin': {'lon_lat': current_waypoint_lon_lat, 'crowflys_distance_and_bearing': {'from_origin': (0, 0)}}, **parks_within_perp_distance, 'destination': {'lon_lat': destination_lon_lat, 'crowflys_distance_and_bearing': {'from_origin': best_fit_origin_to_destination}}}
        # Run the homingAlgo.py module to filter and sort the parks to generate the route
        waypoint_route_order = run_homing_algo(total_waypoints_dict)
        route_waypoints_lon_lat = [total_waypoints_dict[x]['lon_lat'] for x in waypoint_route_order]

        print(route_waypoints_lon_lat)

        # Request the route directions from mapboxDirectionsAPI.py module
        routeGeometry = DirectionsCalculations.returnRouteGeometry(self, route_waypoints_lon_lat)

        return Response([routeGeometry, largestPark])
