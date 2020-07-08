from django.contrib import admin

from .models import Group, CommentStep, CommentStepReply, CommentGroup, CommentGroupFile, CommentGroupReply, Assignment, \
    AssignmentFile, AssignmentWork, AssignmentWorkFile

# Register your models here.
admin.site.register(Group)
admin.site.register(CommentStep)
admin.site.register(CommentStepReply)
admin.site.register(CommentGroup)
admin.site.register(CommentGroupFile)
admin.site.register(CommentGroupReply)
admin.site.register(Assignment)
admin.site.register(AssignmentFile)
admin.site.register(AssignmentWork)
admin.site.register(AssignmentWorkFile)

