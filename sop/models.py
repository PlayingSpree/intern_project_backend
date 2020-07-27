from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework import request
from authapp.models import User
import os.path


def session_file_name(instance, filename):
    return '/'.join(['uploads/post/', str(instance.id), 'cover{0}'.format(os.path.splitext(filename)[1])])


class Session(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    cover = models.ImageField(null=True, blank=True, upload_to=session_file_name)
    publish = models.BooleanField(default=False)
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '[Post id:{}] {}'.format(self.id, self.name)

    # Model Save override to set id as filename
    def save(self, *args, **kwargs):
        if self.id is None:
            cover = self.cover
            self.cover = None
            super(Session, self).save(*args, **kwargs)
            self.cover = cover
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(Session, self).save(*args, **kwargs)


def course_file_name(instance, filename):
    return '/'.join(['uploads/course/', str(instance.id), 'cover{0}'.format(os.path.splitext(filename)[1])])


class Course(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    cover = models.ImageField(null=True, blank=True, upload_to=course_file_name)
    publish = models.BooleanField(default=False)
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    posts = models.ManyToManyField(Session, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '[Course id:{}] {}'.format(self.id, self.name)

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
    return '/'.join(['uploads/step/', str(instance.step_id.id), filename])


class StepFile(models.Model):
    step_id = models.ForeignKey('Step', on_delete=models.CASCADE)
    file = models.FileField(null=True, upload_to=stepfile_file_name)

    def __str__(self):
        return '[StepFile id:{} step_id:{}] {}'.format(self.id, self.step_id, self.file)


def step_file_name(instance, filename):
    return '/'.join(['uploads/step/', str(instance.id), 'cover{0}'.format(os.path.splitext(filename)[1])])


class Step(models.Model):
    name = models.CharField(max_length=64)
    textcontent = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    cover_type = models.IntegerField(default=0,
                                     validators=[MaxValueValidator(2), MinValueValidator(0)])  # 0=None 1=Image 2=Video
    cover_file = models.FileField(null=True, upload_to=step_file_name)
    post_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '[Step id:{}] {}'.format(self.id, self.name)

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
    post_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    # course_id = models.ForeignKey(Course, default=Course.objects.none(), on_delete=models.CASCADE)

    def __str__(self):
        return '[SopHistory id:{}] User id [{}] read post id [{}] at {}'.format(self.id, self.user_id, self.post_id,
                                                                                self.datetime)

    # class Meta:
    #     unique_together = ('user_id', 'post_id',)

    @staticmethod
    def push(user_id,post_id):
        # for post in SopHistory.objects.all().count():
        #     if post != post_id:
        # print(SopHistory.objects.filter(post_id))
        return SopHistory.objects.create(user_id=user_id, post_id=post_id).save()

