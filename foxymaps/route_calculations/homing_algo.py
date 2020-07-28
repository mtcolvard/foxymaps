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
    waypoints_lon_lat = {k:v['lon_lat'] for k, v in all_waypoints.items()}
    waypoint_ids = list(all_waypoints.keys())
    waypoints_graph = {}
    for waypoint_id in waypoint_ids:
        waypoints_graph[waypoint_id] = {}
        for each_id in waypoint_ids:
            # populate every waypoint node [waypoint_id] with a list of the distance and angle to all other waypoints [each_id]
            waypoints_graph[waypoint_id][each_id] = crowflys_bearing(waypoints_lon_lat[waypoint_id], waypoints_lon_lat[each_id])
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
        v[1] != 0 and
        v[1] < (waypoints_graph[route_order[-1]]['destination'][1] + math.pi/5) and
        v[1] > (waypoints_graph[route_order[-1]]['destination'][1] - math.pi/5)}
    # Sort to find closest park
        print('route_order', route_order)
        print('angle_filtered_park_options', angle_filtered_park_options)
        next_park = min(angle_filtered_park_options, key=lambda distance: angle_filtered_park_options[distance][0])
        print(next_park)
        route_order.append(next_park)
    return route_order

def crowflys_bearing(startpoint, endpoint):
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
    crowflys = R * c
# BEARING
    y = math.sin(Δλ) * math.cos(φ2)
    x = math.cos(φ1)*math.sin(φ2) - math.sin(φ1)*math.cos(φ2)*math.cos(Δλ)
    θ = math.atan2(y, x)
    return crowflys, θ
