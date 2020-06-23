from django.db import models
from authapp.models import User
import os.path


def post_file_name(instance, filename):
    return '/'.join(['uploads/post/', str(instance.id), 'cover{0}'.format(os.path.splitext(filename)[1])])


class Post(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    cover = models.ImageField(null=True, upload_to=post_file_name)
    publish = models.BooleanField(default=False)
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Model Save override to set id as filename
    def save(self, *args, **kwargs):
        if self.id is None:
            cover = self.cover
            self.cover = None
            super(Post, self).save(*args, **kwargs)
            self.cover = cover
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(Post, self).save(*args, **kwargs)


def course_file_name(instance, filename):
    return '/'.join(['uploads/course/', str(instance.id), 'cover{0}'.format(os.path.splitext(filename)[1])])


class Course(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    cover = models.ImageField(null=True, upload_to=course_file_name)
    publish = models.BooleanField(default=False)
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    posts = models.ManyToManyField(Post)

    # Model Save override to set id as filename
    def save(self, *args, **kwargs):
        if self.id is None:
            cover = self.cover
            self.cover = None
            super(Course, self).save(*args, **kwargs)
            self.cover = cover
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(Course, self).save(*args, **kwargs)


def stepfile_file_name(instance, filename):
    return '/'.join(['uploads/step/', instance.step_id, filename])


class StepFile(models.Model):
    step_id = models.ForeignKey('Step', on_delete=models.CASCADE)
    file = models.FileField(null=True, upload_to=stepfile_file_name)


def step_file_name(instance, filename):
    return '/'.join(['uploads/step/', str(instance.id), 'cover{0}'.format(os.path.splitext(filename)[1])])


class Step(models.Model):
    name = models.CharField(max_length=64)
    textcontent = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    cover_type = models.IntegerField(default=0)  # 0=None 1=Image 2=Video
    cover_file = models.FileField(null=True, upload_to=step_file_name)
    contents = models.ManyToManyField(StepFile)
    post_id = models.ForeignKey(User, on_delete=models.CASCADE)

    # Model Save override to set id as filename
    def save(self, *args, **kwargs):
        if self.id is None:
            cover = self.cover_file
            self.cover_file = None
            super(Step, self).save(*args, **kwargs)
            self.cover_file = cover
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(Step, self).save(*args, **kwargs)


class SopHistory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user_id', 'post_id']
