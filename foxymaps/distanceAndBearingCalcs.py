# import math
#
# class DistanceAndBearing:
#     def crowflys_bearing(self, startpoint, endpoint):
#
#         startpoint_lon = startpoint[0]
#         startpoint_lat = startpoint[1]
#         endpoint_lon = endpoint[0]
#         endpoint_lat = endpoint[1]
#
#         # this converts angles to radians
#         R = 6371000
#         φ1 = startpoint_lat * math.pi/180
#         φ2 = endpoint_lat * math.pi/180
#         Δφ = (endpoint_lat - startpoint_lat) * math.pi/180
#         Δλ = (endpoint_lon - startpoint_lon) * math.pi/180
#
#         # this measures the distance as the crowflys between two points
#         a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
#         c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
#         crowflys = R * c
#
#         # this calculates the compass bearing from point 1 to point 2
#         y = math.sin(Δλ) * math.cos(φ2)
#         x = math.cos(φ1)*math.sin(φ2) - math.sin(φ1)*math.cos(φ2)*math.cos(Δλ)
#         θ = math.atan2(y, x)
#         # bearing = (θ*180/math.pi + 360) % 360
#         return crowflys, θ
#
#     def perpendicular_distance_from_bestfit_line(self, bestFit, waypointFit):
#
#         # this finds the difference between the compass bearing (origin to destination) and the compass bearing (origin to a given waypoint)
#         angle_to_waypoint = math.fabs(bestFit[1] - waypointFit[1])
#
#         # this calculates the perpendicular distance from the bestfit line (origin to destination) and a given waypoint.  it is used to figure out if a point is within the boundingbox formed from the user's rambling_tolerance
#         perp_distance_to_waypoint = waypointFit[0] * math.sin(angle_to_waypoint)
#         return perp_distance_to_waypoint
