from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Store securely using Django's authentication system
    mobile_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    account_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    document_upload = models.FileField(upload_to='customer_documents/', null=True, blank=True)
    is_active=models.BooleanField(default=False)
    def __str__(self):
        return self.customer_name

class Admin(models.Model):
     username = models.CharField(max_length=50, unique=True)
     email = models.EmailField(unique=True)
     password = models.CharField(max_length=100)

class Savings(models.Model):
    
    name = models.CharField(max_length=50)
    phone= models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='pending') 
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # Admin approval status
    is_blocked = models.BooleanField(default=False)   # Admin block status

    def __str__(self):
        return self.customer.customer_name

class Current(models.Model):
    customer_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100) 
    pincode = models.CharField(max_length=100)
    state  = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # Admin approval status
    is_blocked = models.BooleanField(default=False)   # Admin block status

    def __str__(self):
        return self.customer_name

class Fixed(models.Model):
    customer_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100) 
    pincode = models.CharField(max_length=100)
    state  = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # Admin approval status
    is_blocked = models.BooleanField(default=False)   # Admin block status

    def __str__(self):
        return self.customer_name
    
