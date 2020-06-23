from django.urls import include, path
from rest_framework import routers

from .views_group import GroupViewSet

router = routers.DefaultRouter()
router.register('group', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]