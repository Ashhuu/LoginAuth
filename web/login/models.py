from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.


class UserDetails(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=40)
    phone = models.CharField(max_length=13)
    email = models.EmailField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def addtoDB(self, user, passw):
        add = self(username=user, password=passw)
        add.save()