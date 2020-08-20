waypoint_bearing_to_destination ={
'origin': 248.36276386302092,
394: 226.15336637068845,
395: 228.2833385137317,
457: 240.56854526970304,
458: 238.1610281773771,
467: 249.21737293989992,
473: 244.48833992707742,
475: 242.68546317888362,
476: 240.94900722866555,
483: 244.88079788009796,
496: 240.63853108323428,
504: 241.5393585322683,
546: 245.34600051752685,
1304: 235.95219341878476,
1322: 240.33395616507306,
1323: 235.2235420909513,
1624: 264.46924786743443,
1644: 263.0305468751285,
1989: 258.38371775531846,
2030: 267.1709278719074,
2216: 258.4194778899279,
2363: 317.47938006798097,
2385: 253.44213277975325,
2405: 216.1946492770125,
2457: 214.74199543744774,
2482: 241.66755246478527,
2491: 288.5990937394374,
'destination': 0.0}
waypoint_route_order = ['origin', 467, 473, 504, 457, 496, 475, 476, 2482, 2385, 'destination']

# compass_bearing_dict = {}
# for x in waypoint_route_order:
#     compass_bearing_dict[x] = waypoint_bearing_to_destination[x]
compass_bearing_dict = {}
for x in waypoint_route_order:
    compass_bearing_dict.update({x:waypoint_bearing_to_destination[x]})


# print(waypoint_bearing_to_destination[x])
print('compass_bearing_dict', compass_bearing_dict)


# for x in waypoint_route_order:
#     compass_bearing_dict = {[x]:v for k, v in waypoint_bearing_to_destination.items()}

print(compass_bearing_dict)
