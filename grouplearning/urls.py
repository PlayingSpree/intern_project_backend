from django.urls import include, path
from rest_framework import routers

from grouplearning.views_group import GroupViewSet

router = routers.DefaultRouter()
router.register('', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]