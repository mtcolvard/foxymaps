"""
Populate a graph with the distances and angles of the edges from each waypoint (node) to all other waypoints.
Start at the closest waypoint to the origin.
Then run the filtering algorithm to filter out parks not within an certain angle (e.g. 72 degrees) from each waypoint to the destination.
Then sort by the distances to find the next closest waypoint.
Repeat until the destination is the next closest waypoint.
"""
import math

def run_homing_algo(all_waypoints):
    # create a graph with nodes for each waypoint
    # waypoints_lon_lat = {k:[v['lon_lat'],v['size_in_hectares']] for k, v in all_waypoints.items()}
    waypoint_ids = list(all_waypoints.keys())
    waypoints_graph = {}
    for waypoint_id in waypoint_ids:
        waypoints_graph[waypoint_id] = {}
        for each_id in waypoint_ids:
            # populate every waypoint node [waypoint_id] with a list of the distance and angle to all other waypoints [each_id]
            # crowflys_bearing_and_platonic_width = crowflys_distance_and_bearing(waypoints_lon_lat[waypoint_id][0], waypoints_lon_lat[each_id][0], math.sqrt(waypoints_lon_lat[each_id][1]*10000))
            crowflys_distance_bearing_and_platonic_width = crowflys_distance_and_bearing(all_waypoints[waypoint_id]['lon_lat'], all_waypoints[each_id]['lon_lat'], math.sqrt(all_waypoints[each_id]['size_in_hectares']*10000))
            # waypoints_graph[waypoint_id][each_id] = crowflys_distance_and_bearing(waypoints_lon_lat[waypoint_id][0], waypoints_lon_lat[each_id][0], math.sqrt(waypoints_lon_lat[each_id][1]*10000))
            #
            # crowflys_bearing_and_platonic_width = crowflys_distance_and_bearing(waypoints_lon_lat[waypoint_id][0], waypoints_lon_lat[each_id][0], math.sqrt(waypoints_lon_lat[each_id][1]*10000))

            waypoints_graph[waypoint_id][each_id] = {'crowflys_distance': crowflys_distance_bearing_and_platonic_width[0], 'bearing': crowflys_distance_bearing_and_platonic_width[1], 'platonic_width': crowflys_distance_bearing_and_platonic_width[2], 'crowflys_distance_minus_platonic_width': (crowflys_distance_bearing_and_platonic_width[0]-crowflys_distance_bearing_and_platonic_width[2])}
    print('waypoints graph', waypoints_graph)
    # Run filtering algorithm
    waypoint_route_order = filter_graph_by_angle_then_distance(waypoints_graph)
    print('waypoint_route_order', waypoint_route_order)
    return waypoint_route_order

def filter_graph_by_angle_then_distance(waypoints_graph):
    route_order = ['origin']
    next_park = None
    while route_order:
        if next_park == 'destination':
            break
    # Filter out parks not within x degrees from each waypoint to the destination
        angle_filtered_park_options = {k:v for k, v in waypoints_graph[route_order[-1]].items() if
        v['bearing'] != 0 and
        v['bearing'] < (waypoints_graph[route_order[-1]]['destination']['bearing'] + math.pi/5) and
        v['bearing'] > (waypoints_graph[route_order[-1]]['destination']['bearing'] - math.pi/5)}
    # Sort to find closest park
        # print('route_order', route_order)
        print('angle_filtered_park_options', angle_filtered_park_options)

        # next_park = min(angle_filtered_park_options, key=lambda distance: angle_filtered_park_options[distance]['crowflys_distance'])
        next_park = min(angle_filtered_park_options, key=lambda distance: angle_filtered_park_options[distance]['crowflys_distance_minus_platonic_width'])

        # parks_sorted_by_distance = sorted(angle_filtered_park_options, key=lambda distance:angle_filtered_park_options[distance]['crowflys_distance'])
        # closest_park_by_distance = angle_filtered_park_options[parks_sorted_by_distance[0]]
        # if len(parks_sorted_by_distance) > 1:
        #     second_closest_park_by_distance = angle_filtered_park_options[parks_sorted_by_distance[1]]
        # else:
        #     infinity = float('inf')
        #     second_closest_park_by_distance = (infinity, 0, 0)
        # platonic_width_of_second_closest_park_hecarage = math.sqrt(second_closest_park_by_distance[2]*10000)
        # distance_to_closest_park = closest_park_by_distance[0]
        # distance_to_second_closest_park = second_closest_park_by_distance[0]
        # if (distance_to_second_closest_park - platonic_width_of_second_closest_park_hecarage) < distance_to_closest_park:
        #     next_park = parks_sorted_by_distance[1]
        # else:
        #     next_park = parks_sorted_by_distance[0]
        # # print('next park', next_park)
        # # # print('next_park_size', next_park_size)
        # # # print('closest_park_by_distance', closest_park_by_distance)
        # # # print('second_closest_park_by_distance', second_closest_park_by_distance)
        # print('closest park id and distance', [parks_sorted_by_distance[0], distance_to_closest_park])
        # # # print('distance_to_second_closest_park', distance_to_second_closest_park)
        # try:
        #     second_closest_park_id = parks_sorted_by_distance[1]
        # except (IndexError):
        #     second_closest_park_id = 'destination'
        # print('second_closest_park_id and platonic_width', [second_closest_park_id, platonic_width_of_second_closest_park_hecarage])
        # # # print('parks_sorted_by_distance', parks_sorted_by_distance)

        route_order.append(next_park)
    return route_order


def crowflys_distance_and_bearing(startpoint, endpoint, size_in_hectares):
    R = 6371000
    startpoint_lon = startpoint[0]
    startpoint_lat = startpoint[1]
    endpoint_lon = endpoint[0]
    endpoint_lat = endpoint[1]
    φ1 = startpoint_lat * math.pi/180
    φ2 = endpoint_lat * math.pi/180
    Δφ = (endpoint_lat - startpoint_lat) * math.pi/180
    Δλ = (endpoint_lon - startpoint_lon) * math.pi/180
# CROWFLYS
    a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    crowflys_distance = R * c
# BEARING
    y = math.sin(Δλ) * math.cos(φ2)
    x = math.cos(φ1)*math.sin(φ2) - math.sin(φ1)*math.cos(φ2)*math.cos(Δλ)
    θ = math.atan2(y, x)
    return crowflys_distance, θ, size_in_hectares
