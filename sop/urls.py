from django.urls import include, path
from rest_framework import routers

from .views_post import PostViewSet
from .views_step import StepViewSet
from .views_step_file import StepFileViewSet

router = routers.DefaultRouter()
router.register('post', PostViewSet)
router.register('step/file', StepFileViewSet)
router.register('step', StepViewSet)

urlpatterns = [
    path('', include(router.urls)),
]