from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from grouplearning.views_assignment import AssignmentViewSet, AssignmentWorkViewSet, AssignmentWorkFileViewSet, \
    AssignmentFileViewSet
from grouplearning.views_add_users import AddUserViewSet
from grouplearning.views_comments import CommentGroupViewSet, CommentGroupFileViewSet, CommentGroupReplyViewSet
from grouplearning.views_get_member import GetMemberViewSet
from grouplearning.views_group import GroupViewSet

router = routers.DefaultRouter()
router.register('assignment/work/file', AssignmentWorkFileViewSet)
router.register('assignment/work', AssignmentWorkViewSet)
router.register('assignment/file', AssignmentFileViewSet)
router.register('assignment', AssignmentViewSet)
router.register('comment/upload', CommentGroupFileViewSet)
router.register('comment/reply', CommentGroupReplyViewSet)
router.register('comment', CommentGroupViewSet)
router.register('getmember', GetMemberViewSet)
router.register('adduser', AddUserViewSet)
router.register('', GroupViewSet)
urlpatterns = [
    path('', include(router.urls)),

]
