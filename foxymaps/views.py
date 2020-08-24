import math
import requests
# from django.http import Http404
from django.db.models import Avg
from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from mapbox import Geocoder
from .models import Location
from .serializers import LocationSerializer, LocationUpdateSerializer, LocationSpeedSerializer, BoundingBoxSerializer
from .route_calculations.mapbox_directions_API import Mapbox_Directions_API
from .route_calculations.distance_and_bearing import Distance_And_Bearing
from .route_calculations.homing_algo import run_homing_algo
class LocationList(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # queryset = Location.objects.filter(type_of_site="Churchyard").aggregate(Avg('size_in_hectares'))
    # queryset1 = Location.objects.filter(type_of_site="Churchyard").filter(size_in_hectares__lte=0.834)
    # queryset2 = queryset1.aggregate(Avg('size_in_hectares'))
    # queryset1 = Location.objects.filter(type_of_site="Churchyard")
    # queryset2 = queryset1.filter(size_in_hectares__lt=0.334).filter(borough='City of London')
    # queryset3 = queryset1.filter(size_in_hectares__gt=0.834)
    # print('between 0.334 and 0.834',len(queryset1)-len(queryset2)-len(queryset3))
    # print('lessthan 0.334', len(queryset2))
    # print('greaterthan 0.834', len(queryset3))

class LocationDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
class LocationSpeedList(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # queryset = Location.objects.filter(open_to_public="Yes").exclude(size_in_hectares__lt=0.15)
    queryset = Location.objects.filter(open_to_public="No")
    # .filter(type_of_site="Housing/Estate Landscaping")
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

class QueryRouteGeometry(APIView):
    def get(self, _request, route_waypoints_lon_lat_formatted, compass_and_radius_routing_option_formatted):
        bearing_towards_destination = True
        waypoint_exit_radius='45'
        alley_bias = 1
        walkway_bias = 1
        walking_speed = 1.42
        snap_tolerance= 'unlimited'

        mapbox_directions_API_response = self.returnRouteGeometry(_request, route_waypoints_lon_lat_formatted, compass_and_radius_routing_option_formatted, walking_speed, walkway_bias, alley_bias)

        route_coordinates = mapbox_directions_API_response['routes'][0]['geometry']['coordinates']
        route_distance = mapbox_directions_API_response['routes'][0]['distance']
        route_duration = mapbox_directions_API_response['routes'][0]['duration']
        route_geometry = {'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': route_coordinates}, 'properties':{'distance': route_distance, 'duration': route_duration}}

        route_response = {'route_geometry':route_geometry}
        # print("waypoint_route_order_and_graph", waypoint_route_order_and_graph[1])
        return Response(route_response)

    def returnRouteGeometry(self, _request, waypoints, bearings, walking_speed, walkway_bias, alley_bias):
        params = {
            'geometries': 'geojson',
            # 'continue_straight':'false',
            'access_token': 'pk.eyJ1IjoibXRjb2x2YXJkIiwiYSI6ImNrMDgzYndkZjBoanUzb21jaTkzajZjNWEifQ.ocEzAm8Y7a6im_FVc92HjQ',
            'walking_speed': walking_speed,
            'walkway_bias': walkway_bias,
            'alley_bias': alley_bias,
            'bearings': bearings,
            # 'exclude': 'ferry',
            # 'radiuses': snap_to_grid_tolerance,
        }
        response = requests.get(f'https://api.mapbox.com/directions/v5/mapbox/walking/{waypoints}', params=params)
        print('response.url', response.url)
        data = response.json()
        # print('response.json', data)
        return data

class ParksWithinBoundingBox(APIView):
    def __init__(self):
        self.query_all_parks = Location.objects.all()

    def get(self, _request, origin, destination, ramblingTolerance, parkAccessFilter, minParkSize):
        rambling_tolerance = int(ramblingTolerance)
        origin_lon_lat = [float(x) for x in origin.split(',')]
        destination_lon_lat = [float(x) for x in destination.split(',')]
        access_filter = parkAccessFilter
    # parameters
        rambling_tolerance = 1000
        size_in_hectares_filter = float(minParkSize)/100
        angle_filter = math.pi/5
        pi_divisor = 3
        bearing_towards_destination = True
        waypoint_exit_radius='45'
        platonic_width_factor = 1

        alley_bias = 1
        walkway_bias = 1
        walking_speed = 1.42
        snap_tolerance= 'unlimited'

    # calculate the distance and compass bearing from origin to destination
        best_fit_origin_to_destination = Distance_And_Bearing.crowflys_bearing(self, origin_lon_lat, destination_lon_lat)
        origin_to_destination_distance = best_fit_origin_to_destination[0]
        origin_to_destination_bearing = best_fit_origin_to_destination[1]

    # query the database for all parks and filter the query by public access
        # query_all_parks = Location.objects.all()
        parks_open_to_public = self.query_all_parks.filter(open_to_public='Yes')
        parks_open_to_private = self.query_all_parks.exclude(open_to_public='Yes')
        parks_all_serializer = LocationSpeedSerializer(self.query_all_parks, many=True)
        parks_open_to_public_serializer = LocationSpeedSerializer(parks_open_to_public, many=True)
        parks_open_to_private_serializer = LocationSpeedSerializer(parks_open_to_private, many=True)
        parks_all_data = parks_all_serializer.data
        parks_open_to_public_data = parks_open_to_public_serializer.data
        parks_open_to_private_data = parks_open_to_private_serializer.data

        queryset = self.set_park_access_filter(access_filter, parks_all_data, parks_open_to_public_data, parks_open_to_private_data)

        all_parks = self.populate_all_parks_dict(queryset, origin_lon_lat, best_fit_origin_to_destination)

    # create a boundingbox by filtering out all parks not within the rectangle formed by the distance from origin to destingation and the rambling tolerance (e.g. 1000 meters)
        parks_within_perp_distance = self.calculate_parks_within_perp_distance(all_parks, origin_to_destination_distance, origin_to_destination_bearing, rambling_tolerance, size_in_hectares_filter, pi_divisor)
        # print('parks_within_perp_distance length', len(parks_within_perp_distance))
        # print('parks_within_perp_distance', parks_within_perp_distance)

        if len(parks_within_perp_distance) == 0:
            route_waypoints_lon_lat = [origin_lon_lat, destination_lon_lat]
            parks_within_perp_distance_lon_lat = []
            # largest_park = {'name':'the most Direct Route (No convenient parks enroute)'}
            if access_filter == 'privateParks':
                largest_park = 'the most Direct Route  (No private parks enroute)'
            else:
                largest_park = 'the most Direct Route  (No convenient parks enroute)'
            compass_and_radius_routing_option_formatted = ';'
            waypoint_snap_to_road_grid_tolerance = 'unlimited;unlimited'
        else:
        # Mapbox has a limit of 25 waypoints including the origin and destination for calls to thier Directions API
            total_waypoints_dict = self.sort_parks_by_acreage(origin_lon_lat, destination_lon_lat, best_fit_origin_to_destination, parks_within_perp_distance)
        # Run the route_calculations.homing_algo.py module to find route order of the most direct route
            waypoint_route_order_and_graph = run_homing_algo(total_waypoints_dict, angle_filter, platonic_width_factor)
            waypoint_route_order = waypoint_route_order_and_graph[0]
            waypoint_graph = waypoint_route_order_and_graph[1]
        # compass_and_radius_routing_option is a optional parameter on the mapbox directions API which influences the direction a route starts from each waypoint.  it is useful for making sure routes continue traveling in their current direction
            if bearing_towards_destination is True:
                waypoints_bearing_towards_destination = {}
                for x in waypoint_route_order:
                    waypoints_bearing_towards_destination[x] = waypoint_graph[x]['destination']['compass_bearing']
                waypoints_bearing_list = list(waypoints_bearing_towards_destination.values())
                compass_and_radius_routing_option = f',{waypoint_exit_radius};'.join(str(elem) for elem in waypoints_bearing_list)
                compass_and_radius_routing_option_formatted = compass_and_radius_routing_option+f',{waypoint_exit_radius}'
                print('waypoints_bearing_towards_destination', waypoints_bearing_towards_destination)
            else:
                waypoints_bearing_towards_next_waypoint = {}
                count = 0
                while count < (len(waypoint_route_order)-1):
                    for x in waypoint_route_order:
                        if x == 'destination':
                            waypoints_bearing_towards_next_waypoint['destination'] = 0
                            break
                        count += 1
                        waypoint_target = waypoint_route_order[count]
                        waypoints_bearing_towards_next_waypoint[x] = waypoint_graph[x][waypoint_target]['compass_bearing']
                waypoints_bearing_list = list(waypoints_bearing_towards_next_waypoint.values())
                compass_and_radius_routing_option = f',{waypoint_exit_radius};'.join(str(elem) for elem in waypoints_bearing_list)
                compass_and_radius_routing_option_formatted = compass_and_radius_routing_option+f',{waypoint_exit_radius}'
                print('waypoints_bearing_towards_next_waypoint', waypoints_bearing_towards_next_waypoint)

        # waypoint_snap_to_road_grid_radius is an optional parameter on the mapbox directions API which sets a tolerance for how far mapbox is allowed to move the lon_lat waypoint coordinate is the coordinate is not directly on the road grid
            waypoint_snap_to_road_grid_tolerance = f'{snap_tolerance};'*(len(waypoint_route_order)-1)+f'{snap_tolerance}'
            print(waypoint_snap_to_road_grid_tolerance)

        # Determine the largest park to display in the frontend UI
            waypoints_size_in_hectares = {k:v for k, v in total_waypoints_dict.items() if k in waypoint_route_order}
            largest_park_order = sorted(waypoints_size_in_hectares, key=lambda v: waypoints_size_in_hectares[v]['size_in_hectares'])
            if len(waypoint_route_order) == 3:
                largest_park = waypoints_size_in_hectares[largest_park_order[-1]]['name']
            else:
                largest_park = waypoints_size_in_hectares[largest_park_order[-1]]['name']+' and '+waypoints_size_in_hectares[largest_park_order[-2]]['name']
            # print(largest_park)
            route_waypoints_lon_lat = [total_waypoints_dict[x]['lon_lat'] for x in waypoint_route_order]

    # Formatting for displaying parks within the perpendicular distance with pins on the map if necessary for tuning algorithm
        parks_within_perp_distance_lon_lat = list({k:v['lon_lat'] for k, v in parks_within_perp_distance.items()}.values())
        print('parks_within_perp_distance_lon_lat', parks_within_perp_distance_lon_lat)

    # Request the route directions from mapboxDirectionsAPI.py module
        # route_geometry = Mapbox_Directions_API.returnRouteGeometry(self, route_waypoints_lon_lat, walkway_bias, alley_bias)

    #  Request the route directions directly from the Mapbox Directions API
        route_waypoints_lon_lat_string = ';'.join([str(elem) for elem in route_waypoints_lon_lat])
        route_waypoints_lon_lat_formatted = route_waypoints_lon_lat_string.replace('[', '').replace(']', '').replace(' ', '')
# ////////////
        # mapbox_directions_API_response = self.returnRouteGeometry(_request, route_waypoints_lon_lat_formatted, compass_and_radius_routing_option_formatted, walking_speed, walkway_bias, alley_bias, waypoint_snap_to_road_grid_tolerance)
        #
        # route_coordinates = mapbox_directions_API_response['routes'][0]['geometry']['coordinates']
        # route_distance = mapbox_directions_API_response['routes'][0]['distance']
        # route_duration = mapbox_directions_API_response['routes'][0]['duration']
        # route_geometry = {'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': route_coordinates}, 'properties':{'distance': route_distance, 'duration': route_duration}}
        # print('route_geometry', route_geometry)

    # Calculate the midpoint between the origin and the destination
        midpoint = Distance_And_Bearing.calculate_midpoint(self, origin_lon_lat, destination_lon_lat)

    # Return the response to the frontend Directions API call
        # route_response = {'route_geometry':route_geometry, 'largest_park': largest_park, 'midpoint': midpoint, 'pin_display': route_waypoints_lon_lat}
# ////////////////
        # route_response = {'route_geometry':route_geometry, 'largest_park': largest_park, 'midpoint': midpoint, 'pin_display': parks_within_perp_distance_lon_lat}
        route_response = {'largest_park': largest_park, 'midpoint': midpoint, 'route_pins': route_waypoints_lon_lat, 'all_park_pins': parks_within_perp_distance_lon_lat, 'route_waypoints_lon_lat_formatted': route_waypoints_lon_lat_formatted, 'compass_and_radius_routing_option_formatted': compass_and_radius_routing_option_formatted}
        # print("waypoint_route_order_and_graph", waypoint_route_order_and_graph[1])
        return Response(route_response)
# ///////////////////////////////////
    # def returnRouteGeometry(self, _request, waypoints, bearings, walking_speed, walkway_bias, alley_bias, _snap_to_grid_tolerance):
    #     params = {
    #         'geometries': 'geojson',
    #         # 'continue_straight':'false',
    #         'access_token': 'pk.eyJ1IjoibXRjb2x2YXJkIiwiYSI6ImNrMDgzYndkZjBoanUzb21jaTkzajZjNWEifQ.ocEzAm8Y7a6im_FVc92HjQ',
    #         'walking_speed': walking_speed,
    #         'walkway_bias': walkway_bias,
    #         'alley_bias': alley_bias,
    #         'bearings': bearings,
    #         # 'exclude': 'ferry',
    #         # 'radiuses': snap_to_grid_tolerance,
    #     }
    #     response = requests.get(f'https://api.mapbox.com/directions/v5/mapbox/walking/{waypoints}', params=params)
    #     print('response.url', response.url)
    #     data = response.json()
    #     # print('response.json', data)
    #     return data

    def set_park_access_filter(self, access_filter, parks_all_data, parks_open_to_public_data, parks_open_to_private_data):
        if access_filter == 'allParks':
            queryset = parks_all_data
        elif access_filter == 'publicParks':
            queryset = parks_open_to_public_data
        elif access_filter == 'privateParks':
            queryset = parks_open_to_private_data
        return queryset

    def populate_all_parks_dict(self, queryset_data, origin_lon_lat, best_fit_origin_to_destination):
        all_parks = {}
        for park in queryset_data:
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
            'type_of_site': park['type_of_site'],
            'borough': park['borough'],
            'crowflys_distance_and_bearing': crowflys_distance_and_bearing,
            'distance_from_bestfit_line': Distance_And_Bearing.perpendicular_distance_from_bestfit_line(self, best_fit_origin_to_destination, crowflys_distance_and_bearing),
            'size_in_hectares': size_in_hectares_float,
            'listed_structures': park['listed_structures'],
            'nature_conservation_area': park['nature_conservation_area']}
        return all_parks

    def populate_total_waypoints_dict(self, origin_lon_lat, destination_lon_lat, best_fit_origin_to_destination, parks_within_perp_distance):
        total_waypoints_dict = {'origin': {'lon_lat': origin_lon_lat, 'size_in_hectares': 0, 'crowflys_distance_and_bearing': (0, 0)}, **parks_within_perp_distance, 'destination': {'lon_lat': destination_lon_lat, 'size_in_hectares': 0, 'crowflys_distance_and_bearing': best_fit_origin_to_destination}}
        return total_waypoints_dict

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

    def calculate_parks_within_perp_distance(self, all_parks, origin_to_destination_distance, origin_to_destination_bearing, rambling_tolerance, size_in_hectares_filter, pi_divisor):
        parks_within_perp_distance = {
        k:v for (k, v) in all_parks.items() if
        # select only parks within ± 45 degrees of inital bearing towards destination
            v['crowflys_distance_and_bearing'][1] < (origin_to_destination_bearing + math.pi/pi_divisor) and
            v['crowflys_distance_and_bearing'][1] > (origin_to_destination_bearing - math.pi/pi_divisor) and
        # select only parks within the radius from origin to destination
            v['crowflys_distance_and_bearing'][0] < origin_to_destination_distance and
        # select parks within user's tolerance for rambling
            v['distance_from_bestfit_line'] <= rambling_tolerance and
            v['distance_from_bestfit_line'] >= 0
            and
            v['size_in_hectares'] >= size_in_hectares_filter}

            # v['type_of_site'] != 'Square' and
            # (v['size_in_hectares'] >= size_in_hectares_filter or
            # (v['size_in_hectares'] == 0 and v['type_of_site'] != 'Churchyard'))}

            # (v['size_in_hectares'] >= size_in_hectares_filter
            # or
            # (v['size_in_hectares'] == 0 and (v['borough'] != 'City of London' and v['type_of_site'] != 'Square'))
            # or v['size_in_hectares'] > 0 and v['borough'] == 'City of London' and v['type_of_site'] != 'Square' and v['type_of_site'] != 'Churchyard')}

            # (v['size_in_hectares'] >= size_in_hectares_filter or
            # v['size_in_hectares'] == 0)}
            # v['size_in_hectares'] >= size_in_hectares_filter or
            # v['size_in_hectares'] == 0}

        # print('parks_within_perp_distance length', len(parks_within_perp_distance))
        # print('parks_within_perp_distance', parks_within_perp_distance)
        return parks_within_perp_distance
