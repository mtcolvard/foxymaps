from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include('rest_framework.urls')),
    path('api/', include('jwt_auth.urls')),
    path('api/', include('foxymaps.urls')),
    path('', include('frontend.urls'))

]
