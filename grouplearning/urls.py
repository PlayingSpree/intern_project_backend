from django.urls import include, path
from rest_framework import routers

from grouplearning.views_assignment import AssignmentViewSet

router = routers.DefaultRouter()
router.register('assignment', AssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
