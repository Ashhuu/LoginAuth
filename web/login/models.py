from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.


class UserDetails(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=40)
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    token = models.CharField(max_length=100)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def addtoDB(self, user, passw, phone, email):
        add = UserDetails(username=user, password=passw, phone=phone, email=email)
        add.save()

    def delete_everything():
        UserDetails.objects.all().delete()