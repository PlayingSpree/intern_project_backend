from django.urls import include, path
from rest_framework import routers

from .views_course import CourseViewSet
from .views_session import SessionViewSet
from .views_sophistory import SopHistoryViewSet
from .views_step import StepViewSet
from .views_step_file import StepFileViewSet

router = routers.DefaultRouter()
router.register('session', SessionViewSet)
router.register('step/file', StepFileViewSet)
router.register('step', StepViewSet)
router.register('course', CourseViewSet)
router.register('history', SopHistoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
]