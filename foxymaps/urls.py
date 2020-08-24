from django.urls import path
from .views import LocationList, LocationDetail, LocationFilterList, LocationSpeedList, MapGeocoderView, ParksWithinBoundingBox, QueryRouteGeometry

urlpatterns = [
    path('locations/', LocationList.as_view()),
    path('locationsfilter/', LocationFilterList.as_view()),
    path('locations/<int:pk>', LocationDetail.as_view()),
    path('locationsspeed/', LocationSpeedList.as_view()),
    path('mapbox/geocoder/<searchQuery>', MapGeocoderView.as_view()),
    path('parkswithinboundingbox/<origin>/<destination>/<ramblingTolerance>/<parkAccessFilter>/<minParkSize>', ParksWithinBoundingBox.as_view()),
    path('queryroutegeometry/<route_waypoints_lon_lat_formatted>/<compass_and_radius_routing_option_formatted>', QueryRouteGeometry.as_view()),
]
