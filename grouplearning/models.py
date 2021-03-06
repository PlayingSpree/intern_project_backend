import os.path

from django.db import models

# Create your models here.
from intern_project_backend import settings
from authapp.models import User
from sop.models import Course, Step


def group_image_upload(instance, filename):
    return '/'.join(['uploads/group', str(instance.id), 'group_image{0}'.format(os.path.splitext(filename)[1])])


class Group(models.Model):
    group_name = models.CharField(max_length=100)
    group_description = models.CharField(null=True, blank=True, max_length=250)
    user_joined = models.ManyToManyField(User, related_name='user_joined')
    courses = models.ManyToManyField(Course, blank=True)
    group_image = models.ImageField(blank=True, null=True, upload_to=group_image_upload)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['group_name']

    def __str__(self):
        return self.group_name

    # Model Save override to set id as filename
    def save(self, *args, **kwargs):
        if self.id is None:
            group_image = self.group_image
            self.group_image = None
            super(Group, self).save(*args, **kwargs)
            self.group_image = group_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(Group, self).save(*args, **kwargs)


class CommentStep(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    step_id = models.ForeignKey(Step, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_modified']


class CommentStepReply(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_id = models.ForeignKey(CommentStep, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class CommentGroup(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_modified']


def comment_group_file_upload(instance, filename):
    return '/'.join(['uploads/comment', str(instance.id), filename])


class CommentGroupFile(models.Model):
    comment_id = models.ForeignKey(CommentGroup, on_delete=models.CASCADE)
    file = models.FileField(null=True, upload_to=comment_group_file_upload)

    # Model Save override to set id as filename
    def save(self, *args, **kwargs):
        if self.id is None:
            file = self.file
            self.file = None
            super(CommentGroupFile, self).save(*args, **kwargs)
            self.file = file
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(CommentGroupFile, self).save(*args, **kwargs)


class CommentGroupReply(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_id = models.ForeignKey(CommentGroup, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class Assignment(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin')
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    allow_file = models.BooleanField(default=False)


def assignment_file_upload(instance, filename):
    return '/'.join(['uploads/assignment', str(instance.id), filename])


class AssignmentFile(models.Model):
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    file = models.FileField(null=True, upload_to=assignment_file_upload)

    # Model Save override to set id as filename
    def save(self, *args, **kwargs):
        if self.id is None:
            file = self.file
            self.file = None
            super(AssignmentFile, self).save(*args, **kwargs)
            self.file = file
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(AssignmentFile, self).save(*args, **kwargs)


class AssignmentWork(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user_id', 'assignment_id']


def assignment_work_file_upload(instance, filename):
    return '/'.join(['uploads/assignment/work', str(instance.id), filename])


class AssignmentWorkFile(models.Model):
    assignment_work_id = models.ForeignKey(AssignmentWork, on_delete=models.CASCADE)
    file = models.FileField(null=True, upload_to=assignment_work_file_upload)

    # Model Save override to set id as filename
    def save(self, *args, **kwargs):
        if self.id is None:
            file = self.file
            self.file = None
            super(AssignmentWorkFile, self).save(*args, **kwargs)
            self.file = file
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(AssignmentWorkFile, self).save(*args, **kwargs)
