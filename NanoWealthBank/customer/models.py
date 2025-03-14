from django.db import models
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import random
import string
import pyotp
from django.conf import settings


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
    transaction_pin = models.CharField(max_length=6, null=True, blank=True)
    
    def __str__(self):
        return self.customer_name

    def set_pin(self, raw_pin):
        self.pin_hash = make_password(raw_pin)

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin_hash)

    def set_pin(self, pin):
        self.transaction_pin = make_password(pin)  # Hash the PIN
        self.save()

    def verify_pin(self, pin):
        return check_password(pin, self.transaction_pin)  # Verify the PIN

    def save(self, *args, **kwargs):
        if self.transaction_pin:
            # Ensure PIN is stored as a clean string
            self.transaction_pin = str(self.transaction_pin).strip()
        super().save(*args, **kwargs)


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
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'savings_account'


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
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.customer_name

    class Meta:
        db_table = 'current_account'


class LoanApplication(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    )

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
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loan_purpose = models.TextField()
    application_date = models.DateTimeField(default=timezone.now)
    next_payment_date = models.DateTimeField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    credit_score_at_application = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    has_missed_payments = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan Application for {self.name}"


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
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING', verbose_name="Payment Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Transaction Date & Time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Transfer to {self.receiver_name} - {self.receiver_account_number}"

    class Meta:
        db_table = 'transaction'


class FixedDeposit(models.Model):
    customer_name = models.CharField(max_length=100)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.DecimalField(max_digits=5, decimal_places=3)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    maturity_date = models.DateTimeField()
    maturity_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"FD-{self.id}-{self.customer_name}"

    class Meta:
        ordering = ['-start_date']


class ClassicCardApplication(models.Model):
    BRANCH_CHOICES = [
        ('Ernakulam', 'Ernakulam Branch'),
        ('Trivandrum', 'Trivandrum Branch'),
        ('Kottayam', 'Kottayam Branch'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
    ]
    customer_id = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    branch_location = models.CharField(max_length=50, choices=BRANCH_CHOICES, default='Ernakulam')
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    card_number = models.CharField(max_length=16, unique=True, null=True, blank=True)

    class Meta:
        ordering = ['-application_date']

    def __str__(self):
        return f"Classic Card Application - {self.full_name}"
    

class Manager(models.Model):
    manager_id = models.CharField(max_length=9, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.manager_id:
            # Generate manager ID: MGR + 6 random digits
            while True:
                new_id = 'MGR' + ''.join(random.choices(string.digits, k=6))
                if not Manager.objects.filter(manager_id=new_id).exists():
                    self.manager_id = new_id
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.branch}"

    class Meta:
        db_table = 'manager'
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'
    

class CreditScore(models.Model):
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[
            MinValueValidator(300, message="Credit score cannot be less than 300"),
            MaxValueValidator(900, message="Credit score cannot exceed 900")
        ],
        default=300
    )
    last_updated = models.DateTimeField(auto_now=True)
    
    # Credit Score Components
    payment_history = models.IntegerField(default=0)  # Max 200 points
    credit_utilization = models.IntegerField(default=0)  # Max 200 points
    income_factor = models.IntegerField(default=0)  # Max 150 points
    employment_factor = models.IntegerField(default=0)  # Max 100 points
    age_factor = models.IntegerField(default=0)  # Max 100 points

    def calculate_payment_history(self):
        loans = LoanApplication.objects.filter(customer=self.customer)
        score = 0
        
        for loan in loans:
            if loan.status == 'COMPLETED':
                score += 50  # Completed loans
            elif loan.status == 'ACTIVE' and not loan.has_missed_payments:
                score += 30  # Active loans in good standing
            elif loan.has_missed_payments:
                score -= 20  # Penalty for missed payments
                
        return min(score, 200)

    def calculate_credit_utilization(self):
        active_loans = LoanApplication.objects.filter(
            customer=self.customer, 
            status='ACTIVE'
        )
        total_loan_amount = sum(loan.loan_amount_required for loan in active_loans)
        monthly_income = float(self.customer.monthly_income or 0)
        
        if monthly_income == 0:
            return 0
            
        utilization_ratio = total_loan_amount / (monthly_income * 12)  # Annual ratio
        
        if utilization_ratio <= 0.2:
            return 200  # Excellent utilization
        elif utilization_ratio <= 0.4:
            return 150  # Good utilization
        elif utilization_ratio <= 0.6:
            return 100  # Fair utilization
        else:
            return 50   # Poor utilization

    def calculate_income_factor(self):
        monthly_income = float(self.customer.monthly_income or 0)
        annual_income = monthly_income * 12
        
        if annual_income > 1000000:    # > 10 lakhs
            return 150
        elif annual_income > 500000:   # > 5 lakhs
            return 100
        elif annual_income > 300000:   # > 3 lakhs
            return 75
        else:
            return 50

    def calculate_employment_factor(self):
        employment_status = self.customer.employment_status
        
        if employment_status == 'GOVERNMENT':
            return 100
        elif employment_status == 'PRIVATE':
            return 75
        elif employment_status == 'SELF_EMPLOYED':
            return 50
        else:
            return 25

    def calculate_age_factor(self):
        # Assuming you have age field in Customer model
        age = self.customer.age
        
        if 25 <= age <= 45:
            return 100
        elif 46 <= age <= 55:
            return 75
        else:
            return 50

    def update_credit_score(self):
        self.payment_history = self.calculate_payment_history()
        self.credit_utilization = self.calculate_credit_utilization()
        self.income_factor = self.calculate_income_factor()
        self.employment_factor = self.calculate_employment_factor()
        self.age_factor = self.calculate_age_factor()
        
        # Calculate total score (base score of 300 + factor scores)
        base_score = 300
        factor_score = sum([
            self.payment_history,
            self.credit_utilization,
            self.income_factor,
            self.employment_factor,
            self.age_factor
        ])
        
        self.score = base_score + factor_score
        self.score = min(900, max(300, self.score))
        self.save()

    def get_credit_rating(self):
        if self.score >= 750:
            return "Excellent"
        elif self.score >= 650:
            return "Good"
        elif self.score >= 550:
            return "Fair"
        else:
            return "Poor"

    def __str__(self):
        return f"Credit Score for {self.customer}: {self.score}"
    

class UserDocument(models.Model):
    DOCUMENT_TYPES = [
        ('aadhar_card', 'Aadhar Card'),
        ('pan_card', 'PAN Card'),
        ('passport', 'Passport'),
        ('utility_bills', 'Utility Bills'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=50, unique=True)
    document_file = models.FileField(upload_to='documents/')
    is_verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    face_image = models.ImageField(upload_to='faces/', null=True, blank=True)
    has_verified_face = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'document_type']


# class KYCVerification(models.Model):
#     STATUS_CHOICES = [
#         ('PENDING', 'Pending'),
#         ('APPROVED', 'Approved'),
#         ('REJECTED', 'Rejected'),
#         ('EXPIRED', 'Expired'),
#     ]
    
#     DOCUMENT_TYPES = [
#         ('AADHAAR', 'Aadhaar Card'),
#         ('PAN', 'PAN Card'),
#         ('PASSPORT', 'Passport'),
#     ]
    
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     reference_number = models.CharField(max_length=20, unique=True, null=True)
#     document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
#     document_number = models.CharField(max_length=20)
#     document_file = models.FileField(upload_to='kyc_documents/')
#     selfie = models.ImageField(upload_to='kyc_selfies/', null=True)
#     address_proof = models.FileField(upload_to='address_proofs/', null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
#     submission_date = models.DateTimeField(auto_now_add=True)
#     verification_date = models.DateTimeField(null=True)
#     expiry_date = models.DateTimeField(null=True)
#     verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     rejection_reason = models.TextField(null=True, blank=True)
    
#     class Meta:
#         ordering = ['-submission_date']
        
#     def __str__(self):
#         return f"KYC-{self.reference_number} ({self.customer.customer_name})"
        
#     def is_expired(self):
#         if self.expiry_date:
#             return timezone.now() > self.expiry_date
#         return False





