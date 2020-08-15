import math
import requests

# from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.db.models import Q

from .models import Location
from .serializers import LocationSerializer, LocationUpdateSerializer, LocationSpeedSerializer, BoundingBoxSerializer

from mapbox import Geocoder
from .route_calculations.mapbox_directions_API import Mapbox_Directions_API
from .route_calculations.distance_and_bearing import Distance_And_Bearing
from .route_calculations.homing_algo import run_homing_algo

class LocationList(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationSpeedList(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # queryset = Location.objects.filter(open_to_public="Yes").exclude(size_in_hectares__lt=0.15)
    queryset = Location.objects.filter(open_to_public="Yes")
    # queryset = Location.objects.filter(Q(nature_conservation_area="Yes") | ~Q(listed_structures="None")).filter(open_to_public="Yes").filter(size_in_hectares__gte=1.0)
    # queryset = Location.objects.filter(Q(listed_structures="None"),on_eh_national_register="Yes")
    # queryset = Location.objects.get(id=1327)
    # print('queryset Location Speed List',len( queryset))
    # print('queryset', queryset)
    serializer_class = LocationSpeedSerializer

class LocationFilterList(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    """ Filter by the field needed.  Currently set to size_in_hectares_error """
    queryset = Location.objects.all().filter(size_in_hectares_error=True)
    serializer_class = LocationUpdateSerializer

class MapGeocoderView(APIView):
    def get(self, _request, searchQuery):
        geocoder = Geocoder(name='mapbox.places', access_token='pk.eyJ1IjoibXRjb2x2YXJkIiwiYSI6ImNrZDIycDBuaTAyYjQyeG55azNwYzd0ZjMifQ.yYcTjTmpZ89j4vMWS8VdrA')
        response = geocoder.forward(searchQuery, bbox=[-0.542935,51.255636,0.335605,51.726673])
        data = response.json()
        # print(data)
        return Response(data)

# class Mapbox_Directions_API(APIView):
#     def returnRouteGeometry(self, _request, coords):
#         params = {
#             # 'country': 'GB'
#             'geometries': 'geojson',
#             'walkway_bias:1',
#             'alleyway_bias:1',
#             'access_token': 'pk.eyJ1IjoibXRjb2x2YXJkIiwiYSI6ImNrMDgzYndkZjBoanUzb21jaTkzajZjNWEifQ.ocEzAm8Y7a6im_FVc92HjQ'
#         }
#         response = requests.get(f'https://api.mapbox.com/directions/v5/mapbox/walking/{coords}', params=params)
#         print(response.json())
#         data = response.geojson()
#         print(data)
#         # print('DirectionsCalulations', data)
#         return data['features'][0]

class RouteThenBoundingBox(APIView):

    def get(self, _request, origin, destination, ramblingTolerance):
        rambling_tolerance = int(ramblingTolerance)
        rambling_tolerance = 1000
        size_in_hectares_filter = 0.24
        angle_filter = math.pi/5
        platonic_width_factor = 1
        alley_bias = 1
        walkway_bias = 1


        origin_lon_lat = [float(x) for x in origin.split(',')]
        destination_lon_lat = [float(x) for x in destination.split(',')]
    # calculate the distance from origin to destination
        best_fit_origin_to_destination = Distance_And_Bearing.crowflys_bearing(self, origin_lon_lat, destination_lon_lat)
    # query the database for parks open to the public
        queryset = Location.objects.filter(open_to_public='Yes')
        serializer = LocationSpeedSerializer(queryset, many=True)
        response_data = serializer.data
        all_parks = self.populate_all_parks_dict(response_data, origin_lon_lat, best_fit_origin_to_destination)

    # create a boundingbox by filtering out all parks not within the rectangle formed by the distance from origin to destingation and the rambling tolerance (e.g. 1000 meters)
        parks_within_perp_distance = self.calculate_parks_within_perp_distance(all_parks, 'from_origin', 'origin_to_destination', best_fit_origin_to_destination, rambling_tolerance, size_in_hectares_filter)
        # print('parks_within_perp_distance length', len(parks_within_perp_distance))
        print('parks_within_perp_distance', parks_within_perp_distance)

        if len(parks_within_perp_distance) == 0:
            route_waypoints_lon_lat = [origin_lon_lat, destination_lon_lat]
            largest_park = {'name':'the most Direct Route (No convenient parks enroute)'}
        else:
        # Mapbox has a limit of 25 waypoints including the origin and destination for calls to thier Directions API
            total_waypoints_dict = self.sort_parks_by_acreage(origin_lon_lat, destination_lon_lat, best_fit_origin_to_destination, parks_within_perp_distance)

        # Run the route_calculations/homing_algo.py module to find the most direct route
            waypoint_route_return = run_homing_algo(total_waypoints_dict, angle_filter, platonic_width_factor)

            waypoint_route_order = waypoint_route_return[0]
            for x in waypoint_route_order:
                waypoint_bearing_to_destination = {k:v[x]['compass_bearing'] for k, v in waypoint_route_return[1].items()}
            compass_bearing_dict = {k:v for k, v in waypoint_bearing_to_destination.items() if k in waypoint_route_order}
            # count = 0
            # while count <= len(waypoint_route_order):
            #     radius_list = []
            #     radius_angle = '45'
            #     radius_list = radius_list.append(radius_angle)
            #     count = count + 1
            waypoint_bearings_radius = list(zip(compass_bearing_dict.values(), '45'))
            print('waypoint_bearing_to_destination', waypoint_bearing_to_destination)
            print('compass_bearing_list', compass_bearing_dict.values())
            # print('radius_list', radius_list)
            print('waypoint_bearings_radius', waypoint_bearings_radius)

        # Determine the largest park to display in the frontend UI
            waypoints_size_in_hectares = {k:v for k, v in total_waypoints_dict.items() if k in waypoint_route_order}
            largest_park_order = sorted(waypoints_size_in_hectares, key=lambda v: waypoints_size_in_hectares[v]['size_in_hectares'])
            if len(waypoint_route_order) == 3:
                largest_park = waypoints_size_in_hectares[largest_park_order[-1]]['name']
            else:
                largest_park = waypoints_size_in_hectares[largest_park_order[-1]]['name']+' and '+waypoints_size_in_hectares[largest_park_order[-2]]['name']
            print(largest_park)
            route_waypoints_lon_lat = [total_waypoints_dict[x]['lon_lat'] for x in waypoint_route_order]

    # Format parks within the perpendicular distance for display with pins on the map
        parks_within_perp_distance_lon_lat = list({k:v['lon_lat'] for k, v in parks_within_perp_distance.items()}.values())
        print('parks_within_perp_distance lon_lat', parks_within_perp_distance_lon_lat)
        print('route_waypoints_lon_lat', route_waypoints_lon_lat)

    # Request the route directions from mapboxDirectionsAPI.py module
        # route_geometry = Mapbox_Directions_API.returnRouteGeometry(self, route_waypoints_lon_lat, walkway_bias, alley_bias)

        mapbox_directions_API_response = self.returnRouteGeometry(_request, route_waypoints_lon_lat)

        route_coordinates = mapbox_directions_API_response['routes'][0]['geometry']['coordinates']
        route_distance = mapbox_directions_API_response['routes'][0]['distance']
        route_duration = mapbox_directions_API_response['routes'][0]['duration']
        route_geometry = {'type': 'Feature','geometry': {'type': 'LineString', 'coordinates': route_coordinates}, 'properties':{'distance': route_distance, 'duration': route_duration}}
        print('route_geometry', route_geometry)

    # Calculate the midpoint between the origin and the destination
        midpoint = Distance_And_Bearing.calculate_midpoint(self, origin_lon_lat, destination_lon_lat)

    # Return the response to the frontend Directions API call
        route_response = {'route_geometry':route_geometry, 'largest_park': largest_park, 'midpoint': midpoint, 'parks_within_perp_distance_lon_lat': route_waypoints_lon_lat}
        return Response(route_response)

    def returnRouteGeometry(self, _request, route_waypoints_lon_lat):
        route_waypoints_string = ','.join([str(elem) for elem in route_waypoints_lon_lat])
        coords = route_waypoints_string.replace('[', '').replace(']', '').replace(' ', '')
        # bearings='336,45;334,45;336,45;328,45;333,45;344,45;342,45;343,45;332,45;339,45;337,45;340,45;340,45;339,45;338,45;337,45;338,45;45,45'
        params = {
            # 'country': 'GB'
            'geometries': 'geojson',
            'continue_straight':'false',
            'access_token': 'pk.eyJ1IjoibXRjb2x2YXJkIiwiYSI6ImNrMDgzYndkZjBoanUzb21jaTkzajZjNWEifQ.ocEzAm8Y7a6im_FVc92HjQ',
            'walkway_bias':1,
            'alley_bias':1,
        }
        response = requests.get(f'https://api.mapbox.com/directions/v5/mapbox/walking/{coords}', params=params)
        # ,data=bearings)
        print(response.url)
        data = response.json()
        return data

    def populate_all_parks_dict(self, response_data, origin_lon_lat, best_fit_origin_to_destination):

        all_parks = {}
        for park in response_data:
            lon_lat = [park['lon'], park['lat']]
            crowflys_distance_and_bearing = Distance_And_Bearing.crowflys_bearing(self, origin_lon_lat, lon_lat)
            size_in_hectares = park['size_in_hectares']
            try:
                size_in_hectares_float = float(size_in_hectares)
            except (TypeError, ValueError):
                size_in_hectares_float = 0.0

            all_parks[park['id']] = {
            'id':park['id'],
            'name':park['name'],
            'lon_lat': lon_lat,
            'crowflys_distance_and_bearing': {'from_origin': crowflys_distance_and_bearing},
            'distance_from_bestfit_line': {'origin_to_destination': Distance_And_Bearing.perpendicular_distance_from_bestfit_line(self, best_fit_origin_to_destination, crowflys_distance_and_bearing)},
            'size_in_hectares': size_in_hectares_float,
            'listed_structures': park['listed_structures'],
            'nature_conservation_area': park['nature_conservation_area']}
        return all_parks

    def populate_total_waypoints_dict(self, origin_lon_lat, destination_lon_lat, best_fit_origin_to_destination, parks_within_perp_distance):
        total_waypoints_dict = {'origin': {'lon_lat': origin_lon_lat, 'size_in_hectares': 0, 'crowflys_distance_and_bearing': {'from_origin': (0, 0)}}, **parks_within_perp_distance, 'destination': {'lon_lat': destination_lon_lat, 'size_in_hectares': 0, 'crowflys_distance_and_bearing': {'from_origin': best_fit_origin_to_destination}}}
        return total_waypoints_dict

    def calculate_parks_within_perp_distance(self, all_parks, orientation, journey_leg, best_fit, rambling_tolerance, size_in_hectares_filter):
        parks_within_perp_distance = {
        k:v for (k, v) in all_parks.items() if
        # select only parks within ± 45 degrees of inital bearing towards destination
            v['crowflys_distance_and_bearing'][orientation][1] < (best_fit[1] + math.pi/4) and
            v['crowflys_distance_and_bearing'][orientation][1] > (best_fit[1] - math.pi/4) and
        # select only parks within the radius from origin to destination
            v['crowflys_distance_and_bearing'][orientation][0] < best_fit[0] and
        # select parks within user's tolerance for rambling
            v['distance_from_bestfit_line'][journey_leg] <= rambling_tolerance and
            v['distance_from_bestfit_line'][journey_leg] >= 0 and
            v['size_in_hectares'] >= size_in_hectares_filter}
        print('parks_within_perp_distance length', len(parks_within_perp_distance))
        return parks_within_perp_distance

    def sort_parks_by_acreage(self, origin_lon_lat, destination_lon_lat, best_fit_origin_to_destination, parks_within_perp_distance):
        # mapbox only allows 25 waypoints including origin and destination so we sort and then slice off the 23 largest parks.
        # if len(parks_within_perp_distance) > 23:
        #     waypoints_sorted_by_acreage = sorted(parks_within_perp_distance.keys(), key=lambda y: (parks_within_perp_distance[y]['size_in_hectares']))
        #     # print('waypoints_sorted_by_acreage', waypoints_sorted_by_acreage)
        #     waypoints_sliced_by_acreage = waypoints_sorted_by_acreage[-23:]
        #     total_waypoints_sorted_by_acreage = {k:v for k, v in parks_within_perp_distance.items() if k in waypoints_sliced_by_acreage}
        #     total_waypoints_dict = self.populate_total_waypoints_dict(origin_lon_lat, destination_lon_lat, best_fit_origin_to_destination, total_waypoints_sorted_by_acreage)
        # else:
        #     total_waypoints_dict = self.populate_total_waypoints_dict(origin_lon_lat, destination_lon_lat, best_fit_origin_to_destination, parks_within_perp_distance)
        total_waypoints_dict = self.populate_total_waypoints_dict(origin_lon_lat, destination_lon_lat, best_fit_origin_to_destination, parks_within_perp_distance)

        return total_waypoints_dict
