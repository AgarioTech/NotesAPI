from django.urls import path, include
from rest_framework import routers

from api.v1.users.views import UserViewSet

routers = routers.DefaultRouter()
routers.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(routers.urls)),
    path('api-auth/', include('rest_framework.urls'))
]