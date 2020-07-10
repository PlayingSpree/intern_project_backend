import os

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

def user_image_upload(instance, filename):
    return '/'.join(['uploads/user', str(instance.id), filename])


class User(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    phone = models.CharField(null=True, blank=True, max_length=255)
    image = models.ImageField(null=True, upload_to=user_image_upload)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    def get_username(self):
        return self.email

    # Model Save override to set id as filename
    def save(self, *args, **kwargs):
        if self.id is None:
            image = self.image
            self.image = None
            super(User, self).save(*args, **kwargs)
            self.image = image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(User, self).save(*args, **kwargs)

