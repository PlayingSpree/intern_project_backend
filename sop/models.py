from django.db import models
from authapp.models import User


def post_file_name(instance, filename):
    return '/'.join(['uploads/post/', instance.id, 'cover', filename])


class Post(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    cover = models.ImageField(null=True, upload_to=post_file_name)
    publish = models.BooleanField(default=False)
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


def course_file_name(instance, filename):
    return '/'.join(['uploads/course/', instance.id, 'cover', filename])


class Course(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    cover = models.ImageField(null=True, upload_to=course_file_name)
    publish = models.BooleanField(default=False)
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    posts = models.ManyToManyField(Post)


def stepfile_file_name(instance, filename):
    return '/'.join(['uploads/step/', instance.step_id, filename])


class StepFile(models.Model):
    step_id = models.ForeignKey('Step', on_delete=models.CASCADE)
    file = models.FileField(null=True, upload_to=stepfile_file_name)


def step_file_name(instance, filename):
    return '/'.join(['uploads/step/', instance.id, 'cover', filename])


class Step(models.Model):
    name = models.CharField(max_length=64)
    textcontent = models.TextField()
    link = models.TextField()
    cover_type = models.IntegerField(default=0)  # 0=None 1=Image 2=Video
    cover_file = models.FileField(null=True, upload_to=step_file_name)
    contents = models.ManyToManyField(StepFile)
    post_id = models.ForeignKey(User, on_delete=models.CASCADE)


class SopHistory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user_id', 'post_id']
