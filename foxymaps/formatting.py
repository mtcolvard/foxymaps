# waypoint_route_order = ['origin', 907, 899, 901, 864, 1342, 1327, 'destination']
# mystring = '45;'*(len(waypoint_route_order)-1)+'45'
# print(mystring)
#
# waypoints_bearing_towards_destination {'origin': 283.16754177196884, 889: 278.8086586715406, 891: 280.08417957431504, 868: 272.30304463042944, 908: 265.22005254437863, 853: 271.55266891772715, 1330: 250.19969765660196, 'destination': 0.0}

route_waypoints_lon_lat = [-0.07089000000000001,51.518947499999996,-0.07810205040325,51.516487475579,-0.079117100058409,51.509489894392,-0.09067900000000001,51.5055055]

route_waypoints_lon_lat_string = ';'.join([str(elem) for elem in route_waypoints_lon_lat])
route_waypoints_lon_lat_formatted = route_waypoints_lon_lat_string.replace('[', '').replace(']', '').replace(' ', '')

# waypoint_bearing_to_destination compass_bearing {'origin': 248.36276386302092, 467: 249.21737293989992, 473: 244.48833992707742, 504: 241.5393585322683, 457: 240.56854526970304, 496: 240.63853108323428, 475: 242.68546317888362, 476: 240.94900722866555, 2482: 241.66755246478527, 2385: 253.44213277975325, 'destination': 0.0}
#
# waypoint_bearing_to_destination compass_bearing {'origin': 248.36276386302092, 467: 249.21737293989992, 473: 244.48833992707742, 504: 241.5393585322683, 457: 240.56854526970304, 496: 240.63853108323428, 475: 242.68546317888362, 476: 240.94900722866555, 2482: 241.66755246478527, 2385: 253.44213277975325, 'destination': 0.0}
#
#
#
# waypoint_bearing_to_destination ={
# 'origin': 248.36276386302092,
# 394: 226.15336637068845,
# 395: 228.2833385137317,
# 457: 240.56854526970304,
# 458: 238.1610281773771,
# 467: 249.21737293989992,
# 473: 244.48833992707742,
# 475: 242.68546317888362,
# 476: 240.94900722866555,
# 483: 244.88079788009796,
# 496: 240.63853108323428,
# 504: 241.5393585322683,
# 546: 245.34600051752685,
# 1304: 235.95219341878476,
# 1322: 240.33395616507306,
# 1323: 235.2235420909513,
# 1624: 264.46924786743443,
# 1644: 263.0305468751285,
# 1989: 258.38371775531846,
# 2030: 267.1709278719074,
# 2216: 258.4194778899279,
# 2363: 317.47938006798097,
# 2385: 253.44213277975325,
# 2405: 216.1946492770125,
# 2457: 214.74199543744774,
# 2482: 241.66755246478527,
# 2491: 288.5990937394374,
# 'destination': 0.0}
# waypoint_route_order = ['origin', 467, 473, 504, 457, 496, 475, 476, 2482, 2385, 'destination']
#
# # compass_bearing_dict = {}
# # for x in waypoint_route_order:
# #     compass_bearing_dict[x] = waypoint_bearing_to_destination[x]
# compass_bearing_dict = {}
# for x in waypoint_route_order:
#     compass_bearing_dict.update({x:waypoint_bearing_to_destination[x]})
#
#
# # print(waypoint_bearing_to_destination[x])
# print('compass_bearing_dict', compass_bearing_dict)
#
#
# # for x in waypoint_route_order:
# #     compass_bearing_dict = {[x]:v for k, v in waypoint_bearing_to_destination.items()}
#
# print(compass_bearing_dict)
