from django.urls import path
from .views import LocationList, LocationDetail, LocationFilterList, LocationSpeedList, MapGeocoderView, RouteThenBoundingBox

urlpatterns = [
    path('locations/', LocationList.as_view()),
    path('locationsfilter/', LocationFilterList.as_view()),
    path('locations/<int:pk>', LocationDetail.as_view()),
    path('locationsspeed/', LocationSpeedList.as_view()),
    path('mapbox/geocoder/<searchQuery>', MapGeocoderView.as_view()),
    path('routethenboundingbox/<origin>/<destination>/<ramblingTolerance>/<parkAccessFilter>', RouteThenBoundingBox.as_view()),
]
