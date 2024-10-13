from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login  # Avoid name conflict with the view
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .models import Customer,Admin
from django.contrib.auth.views import LogoutView
import random
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime


def home(request):
    return render(request,'home.html')

def accounts(request):
    return render(request, 'accounts.html')

def services(request):
    return render(request, 'services.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Customer, Admin

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Admin, Customer  # Import your models

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user is an Admin first
        try:
            admin = Admin.objects.get(email=email)
            if admin.password == password:
                # Store admin data in session
                request.session['user_id'] = admin.id
                request.session['user_email'] = admin.email
                request.session['user_role'] = 'admin'  # Set role as admin
                request.session['username'] = admin.username

                return redirect('admindashboard')
            else:
                messages.error(request, "Invalid admin credentials.")
                return render(request, 'login.html')

        except Admin.DoesNotExist:
            # Admin not found, proceed to check for Customer
            try:
                customer = Customer.objects.get(email=email)
                if customer.password == password:
                    if customer.is_active:
                        # Store customer data in session
                        request.session['user_id'] = customer.id
                        request.session['user_email'] = customer.email
                        request.session['user_role'] = 'customer'  # Set role as customer
                        request.session['username'] = customer.username

                        return redirect('userdashboard')
                    else:
                        messages.error(request, "Customer Not Approved Yet.")
                        return render(request, 'login.html')
                else:
                    messages.error(request, "Invalid customer credentials.")
                    return render(request, 'login.html')

            except Customer.DoesNotExist:
                messages.error(request, "No user found with the provided email.")
                return render(request, 'login.html')

    return render(request, 'login.html')



user_pins={}


def dashboard(request):
    context = {
        'user': request.user,
    }
    return render(request, 'customer/userdashboard.html', context)



def personal_banking(request):
    return render(request, 'personal_banking.html')

def business_banking(request):
    return render(request, 'business_banking.html')


#Sign Up
import random;

import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from .models import Customer

user_pin = {}
user_code = {}

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        mobile = request.POST.get('mobilenum')
        customer_name = request.POST.get('customername')

        # Create a new user
        user = Customer(
            username=username,
            password=make_password(password),  # Hash the password for security
            email=email,
            date_of_birth=dob,  # Ensure your model has this field
            mobile_number=mobile,  # Ensure your model has this field
            customer_name=customer_name  # Ensure your model has this field
        )
        user.save()
        
        if user:
            # Generate a random 4-digit verification code
            code = random.randint(1000, 9999)
            user_code[email] = code  # Store the code

            # Send email with the code
            send_mail(
                'Account Verification Code',
                f'Your verification code is {code}.',
                settings.EMAIL_HOST_USER,  # Use your configured email host user
                [email],
                fail_silently=False,
            )
        
            # After saving, redirect to the verification page
            return redirect('verify_code', email=email)
    
    return render(request, 'signup.html')  # Render your signup template


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')  # Redirect to login after successful verification
    else:
        return render(request, 'email_verification_failed.html')
    
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your email has been verified. You can now log in.")
        return redirect('login')
    else:
        return render(request, 'email_verification_failed.html')
    


#def dashboard(request):
    #return render(request, 'customer/userdashboard.html', {'user': request.user})


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

  # Redirect to login page if not logged in
def userdashboard(request):
    # Your dashboard logic here
    user = request.session.get('user_id')
    if user is None:  # Check if user_id is not in the session
        return redirect('login')  # Redirect to login view instead of rendering it
    else:
        return render(request, 'userdashboard.html')

 


class ForgotPasswordView(TemplateView):
    template_name = 'forgotpassword.html'

def forgot_password(request):
     if request.method == 'POST':
        email = request.POST.get('email')

        # Check if the customer exists in the database
        try:
            check = Customer.objects.get(email=email)

            if check:
                # Generate a random 4-digit verification code
                code = random.randint(1000, 9999)
                user_pin[email] = code  # Store the code

                # Send email with the code
                send_mail(
                    'Account Verification Code',
                    f'Your verification code is {code}.',
                    'admin@yourdomain.com',  # Replace with your domain
                    [email],
                    fail_silently=False,
                )

                # Redirect to the verification page
                return redirect('verify_forgotcode', email=email)
        except Exception as e:
            messages.error(request, 'An error occurred. Please try again.')
            print(e)

     return render(request, 'forgotpassword.html')

#def verify_code(request, email):
    #if request.method == 'POST':
        #input_code = request.POST.get('verification_code')
        #if user_code.get(email) == int(input_code):
            # Code is correct, proceed with account activation or login
            #del user_code[email]  # Remove the code after verification
            #return redirect('signup_success')  # Redirect to a success page
        #else:
            # Handle invalid code case
            #return render(request, 'verify_code.html', {'error': 'Invalid verification code.'})
    
    #return render(request, 'verify_code.html')  # Render your verification template 
def verify_code(request, email):
    
    if request.method == 'POST':
        entered_code = request.POST.get('pin')
        correct_code = user_code.get(email)

        if correct_code and str(entered_code) == str(correct_code):
            # Redirect to reset password page if the code is correct
            return render(request,'signup_confirmation.html')
        else:
            messages.error(request, 'Invalid code. Please try again.')        # Verification logic here
    return render(request, 'verify_code.html', {'email': email})


def verifyforgotcode(request, email):
    if request.method == 'POST':
        entered_code = request.POST.get('pin')
        correct_code = user_pin.get(email)

        if correct_code and str(entered_code) == str(correct_code):
            # Redirect to reset password page if the code is correct
            return redirect('reset_password', email=email)
        else:
            messages.error(request, 'Invalid code. Please try again.')

    # For GET requests or after an unsuccessful POST, render the verification page
    return render(request, 'forgot_verifycode.html', {'email': email})


def reset_password(request, email):
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password')
        new_password2 = request.POST.get('confirm_password')

        if new_password1 == new_password2:
            try:
                user = Customer.objects.get(email=email)
                user.password=new_password1  # Use set_password to hash the password correctly
                user.save()  # Save the changes to the database
                messages.success(request, 'Password has been reset successfully.')
                return redirect('login')
            except Customer.DoesNotExist:
                messages.error(request, 'Invalid user.')
                return render(request, 'reset_password.html', {'email': email})
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'reset_password.html', {'email': email})

    # If the request method is GET, render the reset password form
    return render(request, 'reset_password.html', {'email': email})

def admin_dashboard(request):
    pending_customers = Customer.objects.filter(is_active=False)  # Pending approval requests
    customers = Customer.objects.all()
    return render(request, 'admin_dashboard.html', {'pending_customers': pending_customers,'customers': customers })

def approve_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.is_active = True
    customer.save()
    if customer:
        messages.success(request, f'Customer {customer.customer_name} has been approved.')
        return redirect('admindashboard')
    return redirect('admin_dashboard')

def block_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.is_active = not customer.is_active  # Toggle active status
    customer.save()
    if customer:
        messages.success(request, f'Customer {customer.customer_name} has been {"blocked" if not customer.is_active else "unblocked"}.')
        return redirect('admindashboard')
    return redirect('admin_dashboard')

def view_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    return render(request, 'view_customer.html', {'customer': customer})

def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Validate or apply any logic here (e.g., email validation)
        customer.customer_name = name
        customer.email = email
        customer.save()

        messages.success(request, f'Customer {customer.customer_name} has been updated.')
        return redirect('admindashboard')

    return render(request, 'edit_customer.html', {'customer': customer})

import random
import string

def generate_account_number():
    return ''.join(random.choices(string.digits, k=10))  # 10-digit account number

def generate_user_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # 8-character user ID

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))  # 12-character password


import random
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def create_user_account(request):
    if request.method == 'POST':
        # Assuming you have already obtained the username, email, etc.
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Generate account number (random 10-digit number)
        account_number = random.randint(1000000000, 9999999999)

        # Hash the password before storing
        hashed_password = make_password(password)

        # Create a new user
        user = User.objects.create(username=username, email=email, password=hashed_password)

        # Save account number (assuming you have a custom user model or profile)
        # user.profile.account_number = account_number
        # user.profile.save()

        # Send email
        send_confirmation_email(user, account_number, password)

        return redirect('success')  # Redirect after successful account creation

    return render(request, 'create_account.html')


from django.core.mail import EmailMessage

def send_confirmation_email(user, account_number, password):
    # Subject and message for the email
    subject = 'Your Account has been Created'
    message = f"""
    Hello {user.username},

    Your account has been successfully created. Here are your account details:

    Account Number: {account_number}
    Username: {user.username}
    Password: {password}

    Please keep this information safe.

    Thank you for banking with us!

    Best regards,
    Your Bank Team
    """

    # Sending the email
    email = EmailMessage(
        subject,
        message,
        to=[user.email]  # Send to the registered email address
    )
    email.send()


#Savings Account
from django.shortcuts import render

def savings_account(request):
    return render(request, 'savings_account.html')  

from django.shortcuts import render, redirect
from django.http import HttpResponse

# View for displaying the Apply Online form
def savings_application(request):
    return render(request, 'savings_application.html')

# View for handling form submission
def submit_registration(request):
    if request.method == 'POST':
        # Collect the form data
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']
        state = request.POST['state']
        district = request.POST['district']
        account_type = request.POST['account_type']

        # You can add logic to save the data to a database, send an email, etc.

        # For now, we'll just return a simple response
        return HttpResponse(f"Thank you, {name}. Your application for {account_type} account has been received.")


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Customer
from django.urls import reverse

# View for customer login requests
def customer_login_requests(request):
    pending_customers = Customer.objects.filter(is_active=False)
    return render(request, 'admin_dashboard.html', {'pending_customers': pending_customers})

# Approve customer
def approve_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.is_active = True
    customer.save()
    return redirect(reverse('customer_login_requests'))

# View for customer list
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'admin_dashboard.html', {'customers': customers})

# Block/Unblock customer
def block_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.is_active = not customer.is_active
    customer.save()
    return redirect(reverse('customer_list'))

# from django.shortcuts import render
# from .models import Savings  # Assuming you have a SavingsAccount model

# def account_approval_view(request):
#     pending_accounts = Savings.objects.filter(is_active='false')  # Adjust based on your model's status field
#     return render(request, 'admin_dashboard.html', {'pending_accounts': pending_accounts})

def savings_interest(request):
    return render(request, 'savings_interest.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Savings
from django.contrib import messages

# @login_required
def savings_accounts(request):
    print("hello")
    if request.method == 'POST':
        # Get the form data from the request
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        district = request.POST.get('district')
        account_type = request.POST.get('account_type')

        
        print(f"Form Data: Name={name}, Phone={phone}, Email={email}, Address={address}, City={city}, Pincode={pincode}, State={state}, District={district}, Account Type={account_type}")


        # Check if all required fields are provided
        # if name and phone and email and address and city and pincode and state and district and account_type:
        #     print("condition")
    # Create a savings account request and set it as pending
        user=request.session.get('username') 
        account_request = Savings(
                                        user=user,  # Get the current authenticated user
                                        name=name,
                                        phone=phone,
                                        email=email,
                                        address=address,
                                        city=city,
                                        pincode=pincode,
                                        state=state,
                                        district=district,
                                        account_type=account_type  # Ensure account_type is properly handled
                                        )
        account_request.save()

            # Notify the user that their request is pending admin approval
        messages.success(request, 'Your savings account request has been submitted and is pending approval.')

        return render(request, 'customer/userdashboard.html')  # Redirect to the user's dashboard or any desired page
    else:
            # If some fields are missing, show an error message
         messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'savings_application.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    # If the user is authenticated, log them out
    if request.method == 'POST':
        request.session.flush() 
        logout(request)
        return redirect('login')  # Ensure 'login' matches the name in your URLs
    else:
        # Optionally, you can also handle a GET request
        return redirect('login')  # Redirect to login page
    
def transactions(request):
    return render(request, 'transactions.html')

def transactions_view(request):
    # Initialize balance and transaction history in the session if they don't exist
    if 'balance' not in request.session:
        request.session['balance'] = 0
    if 'transactions' not in request.session:
        request.session['transactions'] = []

    # Handle POST requests for deposit or withdrawal
    if request.method == 'POST':
        if 'deposit-amount' in request.POST:
            # Process deposit
            deposit_amount = float(request.POST.get('deposit-amount'))
            request.session['balance'] += deposit_amount

            # Store the transaction in session
            request.session['transactions'].append({
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'Deposit',
                'amount': deposit_amount,
                'balance': request.session['balance']
            })
            request.session.modified = True
            messages.success(request, f'Amount {deposit_amount} has been deposited successfully!')

        elif 'withdrawal-amount' in request.POST:
            # Process withdrawal
            withdrawal_amount = float(request.POST.get('withdrawal-amount'))
            if withdrawal_amount <= request.session['balance']:
                request.session['balance'] -= withdrawal_amount

                # Store the transaction in session
                request.session['transactions'].append({
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'type': 'Withdrawal',
                    'amount': withdrawal_amount,
                    'balance': request.session['balance']
                })
                request.session.modified = True
                messages.success(request, f'Amount {withdrawal_amount} has been withdrawn successfully!')
            else:
                messages.error(request, 'Insufficient balance for the withdrawal!')

    # Render the template with the current balance and transaction history
    context = {
        'balance': request.session['balance'],
        'transactions': request.session['transactions'],
    }
    return render(request, 'transactions.html', context)


from .models import Savings  # Make sure to import your model

def account_approval_view(request):
    # Fetch all pending savings account requests
    print("hello")
    pending_requests = Savings.objects.filter(is_active=0)
    return render(request, 'admin_dashboard.html', {'pending_requests': pending_requests})


from django.shortcuts import redirect

def approve_savings_account(request, request_id):
    savings_account_request = Savings.objects.get(id=request_id)
    savings_account_request.status = 'approved'
    savings_account_request.save()
    return redirect('account_approval')

def reject_savings_account(request, request_id):
    savings_account_request = Savings.objects.get(id=request_id)
    savings_account_request.status = 'rejected'
    savings_account_request.save()
    return redirect('account_approval')

def pending_savings_account(request, request_id):
    savings_account_request = Savings.objects.get(id=request_id)
    savings_account_request.status = 'pending'
    savings_account_request.save()
    return redirect('account_approval')


#View Profile in dashboard
def view_profile(request):
    return render(request, 'view_profile.html')

#Current Account
def current_account(request):
    return render(request, 'current_account.html')