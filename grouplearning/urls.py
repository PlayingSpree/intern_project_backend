from django.urls import include, path
from rest_framework import routers

from grouplearning.views_assignment import AssignmentViewSet, AssignmentWorkViewSet, AssignmentWorkFileViewSet, \
    AssignmentFileViewSet
from grouplearning.views_course import GroupCourseViewSet

router = routers.DefaultRouter()
router.register('assignment/work/file', AssignmentWorkFileViewSet)
router.register('assignment/work', AssignmentWorkViewSet)
router.register('assignment/file', AssignmentFileViewSet)
router.register('assignment', AssignmentViewSet)
router.register('course', GroupCourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
