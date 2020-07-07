from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from grouplearning.views_add_users import AddUserViewSet
from grouplearning.views_comments import CommentGroupViewSet, CommentGroupFileViewSet
from grouplearning.views_group import GroupViewSet

router = routers.DefaultRouter()
router.register('comment/upload', CommentGroupFileViewSet)
router.register('comment', CommentGroupViewSet)
router.register('adduser', AddUserViewSet)
router.register('', GroupViewSet)
urlpatterns = [
    path('', include(router.urls)),

]