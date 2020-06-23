from django.db import models

# Create your models here.
from intern_project_backend import settings
from authapp.models import User


def group_image_upload(instance, filename):
    return '/'.join(['upload/group/', instance.id, 'grp_image', filename])


class Group(models.Model):
    grp_name = models.CharField(max_length=100, default='')
    grp_description = models.CharField(null=True, max_length=250, default='')
    user_joined = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_joined', null=True)
    grp_image = models.ImageField(null=True, upload_to=group_image_upload)
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    REQUIRED_FIELDS = ['grp_name']

    class Meta:
        ordering = ['grp_name']

    def __str__(self):
        return self.grp_name


class GroupRole(models.Model):
    group_id = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='group_id', null=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_id', null=True)
    role = models.CharField(max_length=100, default='')


class Course(models.Model):
    grp_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='grp_id', null=True)
    authorized_role = models.CharField(max_length=100, default='')
    REQUIRED_FIELDS = ['authorized_role']


def course_file_upload(instance, filename):
    return '/'.join(['upload/part/', instance.id, 'vdo_file', filename])


class Video(models.Model):
    vdo_name = models.CharField(max_length=100, default='', unique=True)
    vdo_file = models.FileField(null=True, upload_to=course_file_upload)


def course_image_upload(instance, filename):
    return '/'.join(['upload/course/', instance.id, 'course_image', filename])


class CourseDetail(models.Model):
    course_name = models.CharField(max_length=100, default='', unique=True)
    course_description = models.CharField(max_length=250, null=True, default='')
    course_id = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='course_id', null=True)
    vdo_id = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='vdo_id', null=True)
    publish = models.BooleanField(default=False)
    course_image = models.ImageField(null=True, upload_to=course_image_upload)
    REQUIRED_FIELDS = ['course_name']

    def __str__(self):
        return self.course_name



class Comment(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=100, blank=True, default='')
    rating = models.PositiveIntegerField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user', null=True, blank=True)

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        unique_together = [
            'user', 'course_id'
        ]

    def __str__(self):
        return self.review_text

