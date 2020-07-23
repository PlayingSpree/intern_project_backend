from django.urls import path, include
from rest_framework import routers

from authapp.views import UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('users/', include(router.urls)),
    path('', include('djoser.urls.authtoken')),
]
