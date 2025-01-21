from django.db import models
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User


class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    # Store securely using Django's authentication system
    password = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    document_upload = models.FileField(
        upload_to='customer_documents/', null=True, blank=True)
    pin_hash = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name

    def set_pin(self, raw_pin):
        self.pin_hash = make_password(raw_pin)

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin_hash)


class Admin(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} {self.email}"


class LoanOfficer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Savings(models.Model):
    user_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)
    account_number = models.CharField(
        max_length=20, unique=True, blank=True, null=True
    )
    status = models.CharField(max_length=20, default='pending')
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # Admin approval status
    is_blocked = models.BooleanField(default=False)   # Admin block status
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class Current(models.Model):
    user_id = models.CharField(max_length=50, blank=True, null=True)
    customer_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)
    account_number = models.CharField(
        max_length=6, unique=True, blank=True, null=True
    )
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # Admin approval status
    is_blocked = models.BooleanField(default=False)   # Admin block status
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.customer_name

class LoanApplication(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    employment_status = models.CharField(max_length=20)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    loan_type = models.CharField(max_length=20)
    loan_amount_required = models.DecimalField(max_digits=10, decimal_places=2)
    loan_purpose = models.TextField()
    application_date = models.DateTimeField(default=datetime.now)
    next_payment_date = models.DateTimeField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan Application for {self.name}"



# class Transaction(models.Model):
#     ACCOUNT_TYPE_CHOICES = [
#         ('SAVINGS', 'Savings'),
#         ('CURRENT', 'Current'),
#     ]
#     PAYMENT_STATUS_CHOICES = [
#         ('SUCCESS', 'Success'),
#         ('FAILED', 'Failed'),
#         ('PENDING', 'Pending'),
#     ]
#     user_id = models.CharField(max_length=50, blank=True, null=True)
#     owner_name = models.CharField(max_length=200, blank=True, null=True)
#     owner_account_number = models.CharField(
#         max_length=20, verbose_name="Customer's Account Number")
#     receiver_name = models.CharField(
#         max_length=100, verbose_name="Receiver's Full Name")
#     receiver_account_number = models.CharField(
#         max_length=20, verbose_name="Receiver's Account Number")
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     receiver_account_type = models.CharField(
#         max_length=10,
#         choices=ACCOUNT_TYPE_CHOICES,
#         verbose_name="Type of Receiver's Account"
#     )
#     ifsc_code = models.CharField(max_length=11, verbose_name="IFSC Code")
#     purpose = models.TextField(
#         verbose_name="Purpose of Transfer", null=True, blank=True)

#     payment_id = models.CharField(max_length=255, blank=True, null=True)
#     payment_status = models.CharField(
#         max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING', verbose_name="Payment Status"
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True, verbose_name="Transaction Date & Time")
#     updated_at = models.DateTimeField(
#         auto_now=True, verbose_name="Last Updated")
#     is_approved = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Transfer to {self.receiver_name} - {self.receiver_account_number}"

class Transaction(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('SAVINGS', 'Savings'),
        ('CURRENT', 'Current'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending'),
    ]
    user_id = models.CharField(max_length=50, blank=True, null=True)
    owner_name = models.CharField(max_length=200, blank=True, null=True)
    owner_account_number = models.CharField(max_length=20, verbose_name="Customer's Account Number")
    receiver_name = models.CharField(max_length=100, verbose_name="Receiver's Full Name")
    receiver_account_number = models.CharField(max_length=20, verbose_name="Receiver's Account Number")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receiver_account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, verbose_name="Type of Receiver's Account")
    ifsc_code = models.CharField(max_length=11, verbose_name="IFSC Code")
    purpose = models.TextField(verbose_name="Purpose of Transfer", null=True, blank=True)

    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING', verbose_name="Payment Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Transaction Date & Time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Transfer to {self.receiver_name} - {self.receiver_account_number}"

class FixedDeposit(models.Model):
    user_id = models.CharField(max_length=50, blank=True, null=True)
    customer_name = models.CharField(max_length=100)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # in percentage
    duration_months = models.PositiveIntegerField()  # Duration in months
    start_date = models.DateField(default=timezone.now)
    maturity_date = models.DateField(editable=False)
    maturity_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calculate the maturity date based on duration
        self.maturity_date = self.start_date + timedelta(days=30 * self.duration_months)
        
        # Calculate the maturity amount with compound interest formula
        # A = P * (1 + r/n)^(nt) where P=principal, r=interest rate, t=time in years, n=compounding frequency
        principal = float(self.deposit_amount)
        rate = float(self.interest_rate) / 100  # Convert percentage to decimal
        time = self.duration_months / 12  # Convert months to years
        n = 1  # Assuming yearly compounding for simplicity; you can make it configurable if needed
        maturity_amount = principal * (1 + rate / n) ** (n * time)
        
        # Store calculated maturity amount
        self.maturity_amount = round(maturity_amount, 2)
        
        # Call the parent save method to save the model
        super(FixedDeposit, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - Deposit: {self.deposit_amount} - Maturity: {self.maturity_amount}"
    

class ClassicCardApplication(models.Model):
    BRANCH_CHOICES = [
        ('Mumbai Main', 'Mumbai Main Branch'),
        ('Delhi Central', 'Delhi Central Branch'),
        ('Bangalore Tech', 'Bangalore Tech Park Branch'),
        ('Chennai CBD', 'Chennai CBD Branch'),
        ('Kolkata North', 'Kolkata North Branch'),
        ('Hyderabad Cyber', 'Hyderabad Cyber City Branch'),
        ('Pune West', 'Pune West Branch'),
        ('Ahmedabad City', 'Ahmedabad City Branch'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
    ]

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    branch_location = models.CharField(max_length=50, choices=BRANCH_CHOICES, default='Mumbai Main')
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-application_date']

    def __str__(self):
        return f"Classic Card Application - {self.full_name}"
    
