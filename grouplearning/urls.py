from django.urls import include, path
from rest_framework import routers

from grouplearning.views_assignment import AssignmentViewSet, AssignmentWorkViewSet

router = routers.DefaultRouter()
router.register('assignment/work', AssignmentWorkViewSet)
router.register('assignment', AssignmentViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
