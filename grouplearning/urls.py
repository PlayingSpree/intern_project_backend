from django.urls import include, path
from rest_framework import routers

from .views_group import GroupViewSet

router = routers.DefaultRouter()
router.register('creategroup', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]