from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


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


class Loan(models.Model):
    LOAN_TYPES = [
        ('personal', 'Personal Loan'),
        ('vehicle', 'Vehicle Loan')
    ]

    EMPLOYMENT_STATUS = [
        ('employed', 'Employed'),
        ('unemployed', 'Unemployed')
    ]

    user_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    employment_status = models.CharField(
        max_length=20, choices=EMPLOYMENT_STATUS)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    salary_certificate = models.FileField(
        upload_to='documents/salary_certificates/')
    loan_type = models.CharField(max_length=10, choices=LOAN_TYPES)
    loan_amount_required = models.DecimalField(max_digits=10, decimal_places=2)
    loan_purpose = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True)  # Set to now when created
    next_payment_date = models.DateField(
        default=timezone.now)  # Default value can be changed
    balance_due = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.next_payment_date = self.created_at + \
                timezone.timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.loan_type.capitalize()} Loan"


class Transaction(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('SAVINGS', 'Savings'),
        ('CURRENT', 'Current'),
    ]
    user_id = models.CharField(max_length=50, blank=True, null=True)
    owner_name = models.CharField(max_length=200, blank=True, null=True)
    owner_account_number = models.CharField(
        max_length=20, verbose_name="Customer's Account Number")
    receiver_name = models.CharField(
        max_length=100, verbose_name="Receiver's Full Name")
    receiver_account_number = models.CharField(
        max_length=20, verbose_name="Receiver's Account Number")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receiver_account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPE_CHOICES,
        verbose_name="Type of Receiver's Account"
    )
    ifsc_code = models.CharField(max_length=11, verbose_name="IFSC Code")
    purpose = models.TextField(
        verbose_name="Purpose of Transfer", null=True, blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Transaction Date & Time")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Last Updated")
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