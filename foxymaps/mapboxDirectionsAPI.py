# # from mapbox import Directions
#
# service = Directions(access_token='pk.eyJ1IjoibXRjb2x2YXJkIiwiYSI6ImNrMDgzYndkZjBoanUzb21jaTkzajZjNWEifQ.ocEzAm8Y7a6im_FVc92HjQ')
#
# class DirectionsCalculations:
#
#     def returnRouteGeometry(self, waypoints_list):
#         response = service.directions(waypoints_list, profile='mapbox/walking', walkway_bias=1, alley_bias=1, continue_straight=True)
#         data = response.geojson()
#         # print('DirectionsCalulations', data['features'])
#         print('DirectionsCalulations', data)
#         return data['features'][0]
