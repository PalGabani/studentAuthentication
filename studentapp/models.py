from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class User(AbstractUser):
    sname = models.CharField(max_length=30, blank=True)
    dob = models.DateField(null=True, blank=True)  
    contact = models.IntegerField(null=True, blank=True)  
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField()
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    