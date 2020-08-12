def run_homing_algo(all_waypoints):
    # create a graph with nodes for each waypoint
    waypoints_lon_lat = {k:[v['lon_lat'],v['size_in_hectares']] for k, v in all_waypoints.items()}
    waypoint_ids = list(all_waypoints.keys())
    waypoints_graph = {}
    waypoints_graphed = {}
    for waypoint_id in waypoint_ids:
        waypoints_graph[waypoint_id] = {}
        waypoints_graphed[waypoint_id] = {}
        for each_id in waypoint_ids:
            # populate every waypoint node [waypoint_id] with a list of the distance and angle to all other waypoints [each_id]
            # crowflys_bearing_and_platonic_width =
            # waypoints_graph[waypoint_id][each_id] = crowflys_bearing(waypoints_lon_lat[waypoint_id][0], waypoints_lon_lat[each_id][0], math.sqrt(waypoints_lon_lat[each_id][1]*10000))
            waypoints_graph[waypoint_id][each_id] = crowflys_bearing(waypoints_lon_lat[waypoint_id][0], waypoints_lon_lat[each_id][0], math.sqrt(waypoints_lon_lat[each_id][1]*10000))

            crowflys_bearing_and_platonic_width = crowflys_bearing(waypoints_lon_lat[waypoint_id][0], waypoints_lon_lat[each_id][0], math.sqrt(waypoints_lon_lat[each_id][1]*10000))

            waypoints_graphed[waypoint_id][each_id] = {'crowflys': crowflys_bearing_and_platonic_width[0], 'bearing': crowflys_bearing_and_platonic_width[1], 'platonic_width': crowflys_bearing_and_platonic_width[2]}
    print('waypoints graph', waypoints_graph)
    print('waypoints graphed', waypoints_graphed)
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
        v[1] < (waypoints_graph[route_order[-1]]['destination'][1] + math.pi/4) and
        v[1] > (waypoints_graph[route_order[-1]]['destination'][1] - math.pi/4)}
    # Sort to find closest park
        # print('route_order', route_order)
        print('angle_filtered_park_options', angle_filtered_park_options)

        # next_park = min(angle_filtered_park_options, key=lambda distance: angle_filtered_park_options[distance][0])

        parks_sorted_by_distance = sorted(angle_filtered_park_options, key=lambda distance:angle_filtered_park_options[distance][0])
        closest_park_by_distance = angle_filtered_park_options[parks_sorted_by_distance[0]]
        if len(parks_sorted_by_distance) > 1:
            second_closest_park_by_distance = angle_filtered_park_options[parks_sorted_by_distance[1]]
        else:
            infinity = float('inf')
            second_closest_park_by_distance = (infinity, 0, 0)
        platonic_width_of_second_closest_park_hecarage = math.sqrt(second_closest_park_by_distance[2]*10000)
        distance_to_closest_park = closest_park_by_distance[0]
        distance_to_second_closest_park = second_closest_park_by_distance[0]
        if (distance_to_second_closest_park - platonic_width_of_second_closest_park_hecarage) < distance_to_closest_park:
            next_park = parks_sorted_by_distance[1]
        else:
            next_park = parks_sorted_by_distance[0]
        # print('next park', next_park)
        # # print('next_park_size', next_park_size)
        # # print('closest_park_by_distance', closest_park_by_distance)
        # # print('second_closest_park_by_distance', second_closest_park_by_distance)
        print('closest park id and distance', [parks_sorted_by_distance[0], distance_to_closest_park])
        # # print('distance_to_second_closest_park', distance_to_second_closest_park)
        try:
            second_closest_park_id = parks_sorted_by_distance[1]
        except (IndexError):
            second_closest_park_id = 'destination'
        print('second_closest_park_id and platonic_width', [second_closest_park_id, platonic_width_of_second_closest_park_hecarage])
        # # print('parks_sorted_by_distance', parks_sorted_by_distance)

        route_order.append(next_park)
    return route_order
