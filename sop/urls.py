from django.urls import include, path
from rest_framework import routers

from .views_post import PostViewSet

router = routers.DefaultRouter()
router.register('post', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]