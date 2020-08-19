from mapbox import Directions
# from rest_framework.views import APIView
# # from rest_framework.response import Response
# import requests

service = Directions(access_token='pk.eyJ1IjoibXRjb2x2YXJkIiwiYSI6ImNrZDIycDBuaTAyYjQyeG55azNwYzd0ZjMifQ.yYcTjTmpZ89j4vMWS8VdrA')

class Mapbox_Directions_API:

    def returnRouteGeometry(self, waypoints_list, walkway_bias, alley_bias):
        walk = walkway_bias
        alley = alley_bias

        response = service.directions(waypoints_list, profile='mapbox/walking', continue_straight=True, walking_speed=5, walkway_bias=walk, alley_bias=alley)

        data = response.geojson()
        print('API json', response.json())
        print('API, geojson', data)
        return data['features'][0]


# class DirectionsCalculations(APIView):
#     def get(self, _request, coords):
#         params = {
#             # 'country': 'GB'
#             'geometries': 'geojson',
#             'walkway_bias':1,
#             'alleyway_bias':1,
#             'access_token': 'pk.eyJ1IjoibXRjb2x2YXJkIiwiYSI6ImNrMDgzYndkZjBoanUzb21jaTkzajZjNWEifQ.ocEzAm8Y7a6im_FVc92HjQ'
#         }
#         response = requests.get(f'https://api.mapbox.com/directions/v5/mapbox/walking/{coords}', params=params)
#         # print(response.json())
#         data = response.geojson()
#         # print('DirectionsCalulations', data['features'])
#         print('DirectionsCalulations', data)
#         return data['features'][0]
#         # return Response(response.json())
