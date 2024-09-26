from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Store securely using Django's authentication system
    mobile_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    is_active=models.BooleanField(default=False)
    def __str__(self):
        return self.customer_name
class Admin(models.Model):
     username = models.CharField(max_length=50, unique=True)
     email = models.EmailField(unique=True)
     password = models.CharField(max_length=100)