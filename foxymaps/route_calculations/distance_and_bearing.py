import math

class Distance_And_Bearing:

    # this function measures the distance and compass bearing from a startpoint to an endpoint
    def crowflys_bearing(self, startpoint, endpoint):
        startpoint_lon = startpoint[0]
        startpoint_lat = startpoint[1]
        endpoint_lon = endpoint[0]
        endpoint_lat = endpoint[1]
        φ1 = startpoint_lat * math.pi/180
        φ2 = endpoint_lat * math.pi/180
        Δφ = (endpoint_lat - startpoint_lat) * math.pi/180
        Δλ = (endpoint_lon - startpoint_lon) * math.pi/180
    # this measures the distance as the crowflys from point 1 to point 2
        radius_of_earth = 6371000
        a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        crowflys = c * radius_of_earth 
    # this calculates the compass bearing from point 1 to point 2
        y = math.sin(Δλ) * math.cos(φ2)
        x = math.cos(φ1)*math.sin(φ2) - math.sin(φ1)*math.cos(φ2)*math.cos(Δλ)
        compass_bearing_radians = math.atan2(y, x)
        # compass_bearing_degrees = (compass_bearing_radians*180/math.pi + 360) % 360
        return crowflys, compass_bearing_radians

    # this function calculates the midpoint between a startpoint and an endpoint
    def calculate_midpoint(self, startpoint, endpoint):
        startpoint_lon = startpoint[0]
        startpoint_lat = startpoint[1]
        endpoint_lon = endpoint[0]
        endpoint_lat = endpoint[1]
        φ1 = startpoint_lat * math.pi/180
        φ2 = endpoint_lat * math.pi/180
        λ1 = startpoint_lon * math.pi/180
        λ2 = endpoint_lon * math.pi/180
        bx = math.cos(φ2) * math.cos(λ2 - λ1)
        by = math.cos(φ2) * math.sin(λ2 - λ1)
        φ3 = math.atan2(math.sin(φ1) + math.sin(φ2), math.sqrt((math.cos(φ1) + bx) * (math.cos(φ1) + bx) + by*by))
        λ3 = λ1 + math.atan2(by, math.cos(φ1) + bx)
        midpoint = [λ3*180/math.pi, φ3*180/math.pi]
        return midpoint

    # this function determines the perpendicular distance from the bestfit line (origin to destination) to a given park ("waypoint"). it is used in calculating if a park is within the boundingbox.
    def perpendicular_distance_from_bestfit_line(self, bestFit, waypointFit):
    # this finds the difference between the compass bearing of the origin to the destination  ("bestFit[1]") and the compass bearing of the origin to a given park  "waypointFit[1]"
        angle_to_waypoint = math.fabs(bestFit[1] - waypointFit[1])
    # this finds the perpendicular distance by multiplying the distance from origin to the park ("waypointFit[0]") by the sine of the angle from origin to the park ("angle_to_waypoint")
        perp_distance_to_waypoint = waypointFit[0] * math.sin(angle_to_waypoint)
        return perp_distance_to_waypoint
