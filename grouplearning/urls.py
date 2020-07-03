from django.urls import include, path
from rest_framework import routers

from grouplearning.views_assignment import AssignmentViewSet, AssignmentWorkViewSet, AssignmentWorkFileViewSet, \
    AssignmentFileViewSet

router = routers.DefaultRouter()
router.register('assignment/work/file', AssignmentWorkFileViewSet)
router.register('assignment/work', AssignmentWorkViewSet)
router.register('assignment/file', AssignmentFileViewSet)
router.register('assignment', AssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
