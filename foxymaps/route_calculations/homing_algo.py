"""
Populate a graph with the distances and angles of the edges from each waypoint (node) to all other waypoints.
Start at the closest waypoint to the origin.
Then run the filtering algorithm to filter out parks not within an certain angle (e.g. 72 degrees) from each waypoint to the destination.
Then sort by the distances to find the next closest waypoint.
Repeat until the destination is the next closest waypoint.
"""
import math

def run_homing_algo(all_waypoints, angle_filter_to_next_park, platonic_width_factor):
# create a graph whose nodes represent the waypoints (all the visitable parks enroute to the destination)
    waypoint_ids = list(all_waypoints.keys())
    waypoints_graph = {}
    for waypoint_id in waypoint_ids:
        waypoints_graph[waypoint_id] = {}
        for each_id in waypoint_ids:
        # from each park, calculate the distance-as-the-crowflys and the bearing to every other park.  also calculate the square root each park's area, to get a sortof ideal ("platonic") estimate of how tall or wide each park is.
            crowflys_distance_bearing_and_platonic_width = crowflys_distance_and_bearing(all_waypoints[waypoint_id]['lon_lat'], all_waypoints[each_id]['lon_lat'], (math.sqrt(all_waypoints[each_id]['size_in_hectares']*10000)*platonic_width_factor))
        # populate each node with the above distance-as-the-crowflys, bearing, estimate of the park's width, and a heuristic 'crowflys-distance minus the platonic-width'.
        # This heuristic guesses how important a park might be. At each point along the journey, instead of targeting the absolute next closest park, the algorithm considers how wide each park might be.
        # Thus, a large park somewhat farther away may be prioritized over a closer yet smaller park -- if the distance to the large park minus the large park's width is less than the distance to the closer park minus the closer park's width.
            waypoints_graph[waypoint_id][each_id] = {'crowflys_distance': crowflys_distance_bearing_and_platonic_width[0], 'bearing': crowflys_distance_bearing_and_platonic_width[1], 'compass_bearing':crowflys_distance_bearing_and_platonic_width[3], 'platonic_width': crowflys_distance_bearing_and_platonic_width[2], 'crowflys_distance_minus_platonic_width': (crowflys_distance_bearing_and_platonic_width[0]-crowflys_distance_bearing_and_platonic_width[2])}
# Run filtering algorithm
    waypoint_route_order = filter_graph_by_angle_then_distance(waypoints_graph, angle_filter_to_next_park)
    print('waypoint_route_order length', len(waypoint_route_order))
    print('waypoint_route_order', waypoint_route_order)
    return [waypoint_route_order, waypoints_graph]

def filter_graph_by_angle_then_distance(waypoints_graph, angle_filter_to_next_park):
    route_order = ['origin']
    next_park = None
    while route_order:
        if next_park == 'destination':
            break
    # Filter out parks not within x degrees ('angle_filter_to_next_park') from each waypoint to the destination
        angle_filtered_park_options = {k:v for k, v in waypoints_graph[route_order[-1]].items() if
        v['bearing'] != 0 and
        v['bearing'] < (waypoints_graph[route_order[-1]]['destination']['bearing'] + angle_filter_to_next_park) and
        v['bearing'] > (waypoints_graph[route_order[-1]]['destination']['bearing'] - angle_filter_to_next_park)}
        print('length angle_filtered_park_options', len(angle_filtered_park_options))
    # Sort to find closest park
        next_park = min(angle_filtered_park_options, key=lambda distance: angle_filtered_park_options[distance]['crowflys_distance_minus_platonic_width'])
        route_order.append(next_park)
    return route_order

def crowflys_distance_and_bearing(startpoint, endpoint, size_in_hectares_sqroot):
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
    compass_bearing = (θ*180/math.pi + 360) % 360

    return crowflys_distance, θ, size_in_hectares_sqroot, compass_bearing
