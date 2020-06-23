from django.db import models

# Create your models here.
from intern_project_backend import settings


class Group(models.Model):
    grp_name = models.CharField(max_length=100, default='')
    grp_description = models.CharField(null=True, max_length=250, default='')
    user_joined = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_joined', null=True)
    image = models.ImageField(blank=False, null=False)
    REQUIRED_FIELDS = ['grp_name']

    class Meta:
        ordering = ['grp_name']

    def __str__(self):
        return self.grp_name

#might not work.
class GroupRole(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_id', null=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_id', null=True)
    role = models.CharField(max_length=100, default='')


class Course(models.Model):
    grp_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='grp_id', null=True)
    authorized_role = models.CharField(max_length=100, default='')
    REQUIRED_FIELDS = ['authorized_role']


class CourseDetail(models.Model):
    course_name = models.CharField(max_length=100, default='', unique=True)
    course_description = models.CharField(max_length=250, null=True, default='')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_id', null=True)
    #vdo_id = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='vdo_id', null=True))
    REQUIRED_FIELDS = ['course_name']

    def __str__(self):
        return self.course_name

