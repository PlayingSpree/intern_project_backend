from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from grouplearning.views_add_users import  AmountPartialUpdateView
from grouplearning.views_comments import CommentGroupViewSet, CommentGroupFileViewSet
from grouplearning.views_group import GroupViewSet

router = routers.DefaultRouter()
router.register('', GroupViewSet)
router.register('comment', CommentGroupViewSet)
router.register('comment/upload', CommentGroupFileViewSet)
urlpatterns = [
    path('', include(router.urls)),
    url(r'^model/update-partial/(?P<pk>\d+)/(?P<user_id>\d+)$', AmountPartialUpdateView.as_view(), name='user_joined_partial_update'),
]