from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    is_reviewer = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    backend = 'django.contrib.auth.backends.ModelBackend'