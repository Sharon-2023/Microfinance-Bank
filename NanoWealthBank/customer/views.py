from django.urls import reverse
from .models import FixedDeposit, LoanApplication, Savings  # Make sure to import your model
from django.shortcuts import render, redirect, get_object_or_404
from .models import Admin, Customer, LoanOfficer, Transaction, ClassicCardApplication, Manager, CreditScore
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
import random
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.contrib import messages
from .models import Savings, Current
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from decimal import Decimal
from django.utils import timezone
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import os
import string
from django.core.cache import cache
import requests
import json
import google.generativeai as genai
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum, Count, Avg
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from django.views.decorators.http import require_POST


def home(request):
    return render(request, 'home.html')


def accounts(request):
    return render(request, 'accounts.html')


def services(request):
    return render(request, 'services.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)

        # First check for Manager
        try:
            manager = Manager.objects.get(manager_id=email)
            if check_password(password, manager.password):
                request.session['user_id'] = manager.id
                request.session['user_email'] = manager.email
                request.session['user_role'] = 'manager'
                request.session['username'] = manager.name
                return redirect('managerdashboard')
            else:
                messages.error(request, "Invalid manager credentials.")
                return render(request, 'login.html')
        except Manager.DoesNotExist:
            # If not a manager, check for Admin
            try:
                admin = Admin.objects.get(email=email)
                if admin.password == password:
                    request.session['user_id'] = admin.id
                    request.session['user_email'] = admin.email
                    request.session['user_role'] = 'admin'
                    request.session['username'] = admin.username
                    return redirect('admindashboard')
                else:
                    messages.error(request, "Invalid admin credentials.")
                    return render(request, 'login.html')
            except Admin.DoesNotExist:
                # Check for Loan Officer
                try:
                    loan_officer = LoanOfficer.objects.get(email=email)
                    if loan_officer.password == password:
                        request.session['user_id'] = loan_officer.id
                        request.session['user_email'] = loan_officer.email
                        request.session['user_role'] = 'loan_officer'
                        request.session['username'] = f"{loan_officer.first_name} {loan_officer.last_name}"
                        return redirect('loanofficerdashboard')
                    else:
                        messages.error(request, "Invalid loan officer credentials.")
                        return render(request, 'login.html')
                except LoanOfficer.DoesNotExist:
                    # Finally check for Customer
                    try:
                        customer = Customer.objects.get(email=email)
                        if check_password(password, customer.password):
                            if customer.is_active:
                                request.session['user_id'] = customer.id
                                request.session['user_email'] = customer.email
                                request.session['user_role'] = 'customer'
                                request.session['username'] = customer.username
                                return redirect('userdashboard')
                            else:
                                messages.error(request, "Customer Not Approved Yet.")
                                return render(request, 'login.html')
                        else:
                            messages.error(request, "Invalid customer credentials.")
                            return render(request, 'login.html')
                    except Customer.DoesNotExist:
                        messages.error(request, "No account found with this email.")
                        return render(request, 'login.html')

    return render(request, 'login.html')

user_pins = {}


def dashboard(request):
    user_id = request.session.get('user_id')
    account_number = 0
    saving_account = Savings.objects.filter(user_id=user_id).first()
    current_account = Current.objects.filter(user_id=user_id).first()
    if saving_account:
        account_number = saving_account.account_number
    if current_account:
        account_number = current_account.account_number
    context = {
        'user': request.user,
        "account_number": account_number
    }
    return render(request, 'customer/userdashboard.html', context)


def personal_banking(request):
    return render(request, 'personal_banking.html')


def business_banking(request):
    return render(request, 'business_banking.html')


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
        document_upload = request.FILES.get('document_upload')

        # Create a new user with the generated account number
        user = Customer(
            username=username,
            password=make_password(password),  # Hash the password for security
            email=email,
            date_of_birth=dob,  # Ensure your model has this field
            mobile_number=mobile,  # Ensure your model has this field
            customer_name=customer_name,  # Ensure your model has this field
            # account_number=account_number  # Add the generated account number
            document_upload=document_upload
        )
        user.save()

        if user:
            # Generate a random 4-digit verification code
            code = random.randint(1000, 9999)

            user_code[email] = code  # Store the code

            # Send email with the verification code and account number
            send_mail(
                'Account Verification Code and Details',
                f'Hello {customer_name},\nYour verification code is {code}.',
                settings.EMAIL_HOST_USER,  # Use your configured email host user
                [email],
                fail_silently=False,
            )

            # After saving, redirect to the verification page
            return render(request, 'verify_code.html', {'email': email})

    return render(request, 'signup.html')


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Redirect to login after successful verification
        return redirect('login')
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
        messages.success(
            request, "Your email has been verified. You can now log in.")
        return redirect('login')
    else:
        return render(request, 'email_verification_failed.html')


# def dashboard(request):
    # return render(request, 'customer/userdashboard.html', {'user': request.user})


def userdashboard(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('login')

    # account_number = request.session.get('account_number')
    account = Savings.objects.filter(user_id=user_id, is_approved=True).first()
    account_number = account.account_number if account else None
    return render(request, 'customer/userdashboard.html', {
        'account_number': account_number,
    })


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


def verify_code(request, email):

    if request.method == 'POST':
        entered_code = request.POST.get('pin')
        correct_code = user_code.get(email)

        if correct_code and str(entered_code) == str(correct_code):
            # Redirect to reset password page if the code is correct
            return render(request, 'signup_confirmation.html')
        else:
            messages.error(request, 'Invalid code. Please try again.')
    return render(request, 'verify_code.html')


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
                user.password = new_password1  # Use set_password to hash the password correctly
                user.save()  # Save the changes to the database
                messages.success(
                    request, 'Password has been reset successfully.')
                return redirect('login')
            except Customer.DoesNotExist:
                messages.error(request, 'Invalid user.')
                return render(request, 'reset_password.html', {'email': email})
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'reset_password.html', {'email': email})

    # If the request method is GET, render the reset password form
    return render(request, 'reset_password.html', {'email': email})


def approve_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.is_active = True
    customer.save()
    if customer:
        messages.success(request, f'Customer {customer.customer_name} has been approved.')
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


# Checking if the user is already having an account
def apply_for_account(request):
    if request.method == 'POST':
        if Savings.objects.filter(user=request.user).exists() or Current.objects.filter(user=request.user).exists():
            return render(request, 'error.html', {'message': 'You already have an account.'})

        account_type = request.POST.get('account_type')
        if account_type == 'savings':
            Savings.objects.create(user=request.user)
        elif account_type == 'current':
            Current.objects.create(user=request.user)

        return redirect('success_page')

# View Profile in dashboard


def view_profile(request):
    # Get the user ID from the session
    user_id = request.session.get('user_id')
    user = Customer.objects.get(id=user_id)

    # Get savings and current account details
    saving_bank = Savings.objects.filter(user_id=user.id).first()
    current_bank = Current.objects.filter(user_id=user.id).first()

    # Set not approved message if accounts are not approved
    not_approved_message = None
    if saving_bank and not saving_bank.is_approved:
        not_approved_message = "Your savings account is not approved. Please contact support."
    if current_bank and not current_bank.is_approved:
        not_approved_message = "Your current account is not approved. Please contact support."

    # If the form is submitted, handle POST request to update the profile
    if request.method == 'POST':
        # Get data from the form fields
        customer_name = request.POST.get('customer_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        date_of_birth = request.POST.get('date_of_birth')

        # Update the user's profile data
        user.customer_name = customer_name
        user.email = email
        user.mobile_number = mobile_number
        user.date_of_birth = date_of_birth

        # Save updated information
        user.save()

        # Success message
        messages.success(request, "Profile updated successfully!")

        # Redirect to the profile page to show the updated data
        return redirect('view_profile')

    # Render the profile template with the necessary data
    return render(request, 'customer/view_profile.html', {
        'customer': user,
        'savings_account': saving_bank,
        'current_bank': current_bank,
        'not_approved_message': not_approved_message,
    })


def savings_account(request):
    return render(request, 'customer/savings_account.html')


def savings_application(request):
    user = request.session.get('user_id')
    user_details = Customer.objects.get(id=user)
    return render(request, 'customer/savings_application.html', {'user': user_details})


# Savings application email verification
verification_codes = {}


def send_verification_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Generate a random 6-digit code
            code = str(random.randint(100000, 999999))
            print(code)
            verification_codes[email] = code

            # Send email with verification code
            subject = 'NanoWealthBank - Email Verification'
            message = f'Your verification code is: {code}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                return JsonResponse({'success': True, 'message': 'Verification code sent successfully'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        else:
            return JsonResponse({'success': False, 'message': 'Email is required'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def code_verify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        if email and code:
            stored_code = verification_codes.get(email)
            if stored_code and stored_code == code:
                # Remove the used code
                del verification_codes[email]
                return JsonResponse({'success': True, 'message': 'Verification successful'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid verification code'})
        else:
            return JsonResponse({'success': False, 'message': 'Email and code are required'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@csrf_exempt
def submit_application(request):
    if request.method == 'POST':
        try:
            # Extract data from request.POST
            name = request.POST.get('customerName')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            district = request.POST.get('district')
            pincode = request.POST.get('pinCode')
            account_type = request.POST.get('accountType')

            # Retrieve user_id from session, if available
            user_id = request.session.get('user_id')

            if user_id:
                # Check if a Savings account already exists for the user
                existing_savings = Savings.objects.filter(
                    user_id=user_id).first()

                if existing_savings:
                    return JsonResponse({'success': False, 'message': 'An application already exists for this user.'})

                # Create Savings object with user_id
                savings = Savings(
                    user_id=user_id,
                    name=name,
                    phone=phone,
                    email=email,
                    address=address,
                    city=city,
                    state=state,
                    district=district,
                    pincode=pincode,
                    account_type=account_type
                )
            else:
                # Create Savings object without user_id
                savings = Savings(
                    name=name,
                    phone=phone,
                    email=email,
                    address=address,
                    city=city,
                    state=state,
                    district=district,
                    pincode=pincode,
                    account_type=account_type
                )

            # Save the Savings object
            savings.save()

            # Return success response
            return JsonResponse({'success': True, 'message': 'Application submitted successfully'})
        except Exception as e:
            # Log the error and return a failure response
            print(f"Error saving application: {str(e)}")
            return JsonResponse({'success': False, 'message': 'Failed to submit application'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


def current_application(request):
    user = request.session.get('user_id')
    user_details = Customer.objects.get(id=user)
    return render(request, 'customer/current_application.html',{'user_details':user_details})

def current_account(request):
    return render(request, 'customer/current_account.html')


@csrf_exempt
def submit_application_current(request):
    if request.method == 'POST':
        try:
            # Extract data from request.POST
            name = request.POST.get('customerName')
            print(name)
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pinCode')
            account_type = request.POST.get('accountType')

            user_id = request.session.get('user_id')
            if user_id:
                # Check if a Current account already exists for the user
                existing_current = Current.objects.filter(
                    user_id=user_id).first()

                if existing_current:
                    return JsonResponse({'success': False, 'message': 'An application already exists for this user.'})
                current = Current(
                    user_id=user_id,
                    customer_name=name,
                    mobile_number=phone,
                    email=email,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                    account_type=account_type
                )
            else:
                # Create new Current object
                current = Current(
                    customer_name=name,
                    mobile_number=phone,
                    email=email,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                    account_type=account_type
                )
            current.save()

            return JsonResponse({'success': True, 'message': 'Application submitted successfully'})
        except Exception as e:
            print(f"Error saving application: {str(e)}")
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


def topup_balance(request):
    user = request.session.get('user_id')
    account = {}
    saving_account = Savings.objects.filter(user_id=user).first()
    curr_account = Current.objects.filter(user_id=user).first()
    if saving_account:
        account = saving_account
    if curr_account:
        account = curr_account
    if request.method == 'POST':
        # Get the top-up amount from the form
        topup_amount = request.POST.get('topup_amount')
        try:
            # Convert top-up amount to decimal and add it to the balance
            topup_amount = Decimal(topup_amount)
            if topup_amount > 0:
                account.balance += topup_amount
                account.save()
                return redirect('view_profile')
            else:
                return HttpResponse("Top-up amount must be positive", status=400)
        except ValueError:
            return HttpResponse("Invalid top-up amount", status=400)

    # Render top-up form page if GET request
    return render(request, 'customer/balance_topup.html', {'account': account})
# Transactions


def transactions(request):
    user = request.session.get('user_id')
    account_number = 0
    balance = 0
    saving_account = Savings.objects.filter(user_id=user).first()
    curr_account = Current.objects.filter(user_id=user).first()
    if saving_account:
        account_number = saving_account.account_number
        balance = saving_account.balance
    if curr_account:
        account_number = curr_account.account_number
        balance = curr_account.balance
    transcations = Transaction.objects.filter(user_id=user)
    return render(request, 'customer/transactions.html', {'account_number': account_number, 'transcations': transcations, 'balance': balance})


def download_statement(request):
    period = request.GET.get('period')
    month = request.GET.get('month')
    user = request.session.get('user_id')
    account_number = 0
    userdata = Customer.objects.filter(id=user).first()
    saving_account = Savings.objects.filter(user_id=user).first()
    curr_account = Current.objects.filter(user_id=user).first()
    if saving_account:
        account_number = saving_account.account_number
    if curr_account:
        account_number = curr_account.account_number

    if userdata.date_of_birth:
        password = userdata.date_of_birth.strftime(
            '%d%m%Y')  # e.g., "15061990" for 15th June 1990
    else:
        password = "defaultpassword"

    # Filter transactions based on the selected period
    if period == "last_6_months":
        start_date = timezone.now() - timedelta(days=180)
        transactions = Transaction.objects.filter(created_at__gte=start_date)
    elif period == "specific_month" and month:
        year, month = map(int, month.split('-'))
        start_date = datetime.datetime(year, month, 1)
        end_date = (start_date + timedelta(days=31)).replace(day=1)
        transactions = Transaction.objects.filter(
            created_at__gte=start_date, created_at__lt=end_date
        )
    else:
        transactions = Transaction.objects.none()

    # Generate the PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setTitle("Transaction Statement")

    # Header
    p.drawString(100, 750, "Transaction Statement")
    p.drawString(100, 735, f"Date: {timezone.now().date()}")
    p.drawString(100, 720, f"Account: {account_number}")

    # Table Header
    y = 700
    p.drawString(50, y, "To")
    p.drawString(150, y, "Account Number")
    p.drawString(250, y, "IFSC")
    p.drawString(350, y, "Date")
    p.drawString(450, y, "Amount")
    p.drawString(550, y, "Status")

    # Table Rows
    for transaction in transactions:
        y -= 20
        p.drawString(50, y, transaction.receiver_name)
        p.drawString(150, y, transaction.receiver_account_number)
        p.drawString(250, y, transaction.ifsc_code)
        p.drawString(350, y, transaction.created_at.strftime('%Y-%m-%d'))
        p.drawString(450, y, f"₹ {transaction.amount}")
        status = "Success" if transaction.is_approved else "Failed"
        p.drawString(550, y, status)

        if y < 100:  # Start a new page if space is insufficient
            p.showPage()
            y = 750  # Reset y position

    p.showPage()
    p.save()

    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()

    # Apply password protection
    pdf_reader = PdfReader(io.BytesIO(pdf_data))
    pdf_writer = PdfWriter()
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    # Encrypt the PDF with a password
    pdf_writer.encrypt(password)

    # Create response with protected PDF
    response_buffer = io.BytesIO()
    pdf_writer.write(response_buffer)
    response_buffer.seek(0)

    response = HttpResponse(response_buffer, content_type='application/pdf')
    if period != '':
        print("hi")
        response['Content-Disposition'] = f'attachment; filename="transaction_statement_{period}.pdf"'
    else:
        response['Content-Disposition'] = 'attachment; filename="transaction_statement.pdf"'

    return response


def list_deposits(request):
    user = request.session.get('user_id')
    deposits = FixedDeposit.objects.filter(user_id=user)
    saving_account = Savings.objects.filter(user_id=user).first()
    curr_account = Current.objects.filter(user_id=user).first()
    if saving_account:
        account_number = saving_account.account_number
    if curr_account:
        account_number = curr_account.account_number
    return render(request, 'customer/deposits_list.html', {'deposits': deposits})


def add_deposit(request):
    user = request.session.get('user_id')
    saving_account = Savings.objects.filter(user_id=user).first()
    curr_account = Current.objects.filter(user_id=user).first()
    userdata = Customer.objects.filter(id=user).first()
    if saving_account:
        account_number = saving_account.account_number
    if curr_account:
        account_number = curr_account.account_number
    if request.method == 'POST':
        # Get data from form fields
        customer_name = request.POST.get('customer_name')
        deposit_amount = request.POST.get('deposit_amount')
        interest_rate = request.POST.get('interest_rate')
        duration_months = request.POST.get('duration_months')

        # Convert the form data to the appropriate data types
        deposit_amount = float(deposit_amount) if deposit_amount else 0.0
        interest_rate = float(interest_rate) if interest_rate else 0.0
        duration_months = int(duration_months) if duration_months else 0

        # Create a new FixedDeposit instance
        new_deposit = FixedDeposit(
            user_id=user,
            customer_name=customer_name,
            deposit_amount=deposit_amount,
            interest_rate=interest_rate,
            duration_months=duration_months,
            start_date=timezone.now()
        )

        # Save the instance, which will also calculate maturity date and amount
        new_deposit.save()

        # Redirect to the list of deposits after saving
        return redirect('list_deposits')

    # Render the form page if it's a GET request
    return render(request, 'customer/deposits_add.html', {'userdata': userdata})


@csrf_exempt
def internet_banking(request):
    user = request.session.get('user_id')
    if not user:
        return redirect('login')

    account = {}
    saving_account = Savings.objects.filter(user_id=user).first()
    curr_account = Current.objects.filter(user_id=user).first()
    
    if saving_account:
        account = saving_account
    if curr_account:
        account = curr_account

    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
            current_balance = float(account.balance)

            # Check if sufficient balance
            if amount <= current_balance:
                # Calculate new balance
                new_balance = current_balance - amount

                # Create and save transaction with current_balance
                transaction = Transaction(
                    user_id=user,
                    owner_name=account.name if hasattr(account, 'name') else account.customer_name,
                    owner_account_number=account.account_number,
                    receiver_name=request.POST.get('receiver_name'),
                    receiver_account_number=request.POST.get('receiver_account_number'),
                    amount=amount,
                    receiver_account_type=request.POST.get('receiver_account_type'),
                    ifsc_code=request.POST.get('ifsc_code'),
                    purpose=request.POST.get('purpose'),
                    payment_id=request.POST.get('payment_id'),
                    payment_status='SUCCESS',
                    is_approved=True,
                    current_balance=new_balance  # Store the new balance after transaction
                )
                transaction.save()

                # Update account balance
                account.balance = new_balance
                account.save()

                return JsonResponse({
                    'success': True,
                    'message': 'Transaction saved successfully'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Insufficient balance'
                })

        except Exception as e:
            print(f"Error in transaction: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': str(e)
            })

    return render(request, 'customer/internet_banking.html', {
        'customer': account,
        'account_balance': account.balance if account else 0
    })


def payment_success(request):
    if request.method != 'POST':
        return redirect('home')  # Redirect if not POST
        
    context = {
        'payment_id': request.POST.get('payment_id'),
        'amount': request.POST.get('amount'),
        'receiver_name': request.POST.get('receiver_name'),
        'receiver_account_number': request.POST.get('receiver_account_number'),
        'transaction_date': timezone.now().strftime("%B %d, %Y, %I:%M %p")
    }
    return render(request, 'customer/payment_success.html', context)

# admin dashboard


def admin_dashboard(request):
    context = {
        'total_customers': Customer.objects.count(),
        'total_savings_accounts': Savings.objects.count(),
        'total_current_accounts': Current.objects.count(),
        'total_fixed_deposit': FixedDeposit.objects.count(),
        'total_loans': LoanApplication.objects.count(),
        # Add more context data as needed
    }
    return render(request, 'admin/admin_dashboard.html', context)


def customer_list(request):
    pending_customers = Customer.objects.filter(is_active=False)
    all_customers = Customer.objects.all()

    for customer in pending_customers:
        if customer.document_upload:
            print(f"Customer {customer.id} document URL: {
                  customer.document_upload.url}")
        else:
            print(f"Customer {customer.id} has no document")

    context = {
        'pending_customers': pending_customers,
        'all_customers': all_customers,
    }
    return render(request, 'customer_login_requests.html', context)

# Approve customer


def approve_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.is_active = True
    customer.save()
    return redirect('customer_list')

# Block/Unblock customer


def block_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.is_active = False
    customer.save()
    return redirect('customer_list')


def loanofficer_list(request):
    users = LoanOfficer.objects.all()
    return render(request, 'loanofficer/loanoffecer.html', {"users": users})


def add_loanOfficer_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        errors = []

        # Validation checks
        if not first_name:
            errors.append("First name is required.")
        if not last_name:
            errors.append("Last name is required.")
        if not email:
            errors.append("Email is required.")
        elif LoanOfficer.objects.filter(email=email).exists():
            errors.append("An account with this email already exists.")
        if not password:
            errors.append("Password is required.")

        # If there are errors, re-render the form with error messages
        if errors:
            return render(request, 'create_loan_officer.html', {
                'errors': errors,
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            })

        # Create and save the LoanOfficer if no errors
        LoanOfficer.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        return redirect('loanofficer_list')
    return render(request, 'loanofficer/addloanoffecer.html')


def loan_list(request):
    loans_list = LoanApplication.objects.all()
    return render(request, 'loanlist.html', {'loans': loans_list})


def loan_status_toggle(request, loan_id):
    if request.method == 'POST':
        loan = get_object_or_404(LoanApplication, id=loan_id)
        action = request.POST.get('action')
        if action == 'approve':
            loan.is_approved = True
            loan.balance_due += loan.loan_amount_required
            loan.save()
        elif action == 'reject':
            loan.is_approved = False
            loan.balance_due -= loan.loan_amount_required
            loan.save()

    return redirect('loan_list')


def transactions_list(request):
    transcations = Transaction.objects.all()
    return render(request, 'transcation_list.html', {'transcations': transcations})


def transaction_cancel_or_approve(request, transaction_id):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, id=transaction_id)
        action = request.POST.get('action')
        if action == 'approve':
            transaction.is_approved = True
            transaction.save()
        elif action == 'Cancel':
            transaction.is_approved = False
            transaction.save()

    return redirect('transactions_list')


def savings_account_approval(request):
    pending_accounts = Savings.objects.filter(
        is_approved=False, is_active=False)
    return render(request, 'savings_account_approval.html', {'pending_accounts': pending_accounts})

# Admin- Fixed acoount approval


def loanofficerdashboard(request):
    return render(request, 'loanofficer/loanofficerdashboard.html')


def profile_edit(request):
    # Retrieve user_id from session
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, 'You must be logged in to edit your profile.')
        # Redirect to login if user_id is not in session
        return redirect('login')

    # Fetch the user profile or return 404 if not found
    user = get_object_or_404(LoanOfficer, id=user_id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Validate and update the user's information
        if not first_name or not last_name:
            messages.error(request, 'First name and last name are required.')
        elif LoanOfficer.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(
                request, 'This email is already associated with another account.')
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_edit')

    # Render the edit profile form with the user's current data
    return render(request, 'loanofficer/editprofile.html', {'user': user})


def loan_to_be_approved(request):
    loans = LoanApplication.objects.filter(is_approved=False)
    return render(request, 'loanofficer/loans.html', {'loans': loans})

# View to approve a specific loan


def approve_loan(request, loan_id):
    loan = get_object_or_404(LoanApplication, id=loan_id)

    if request.method == "POST":
        loan.is_approved = True
        loan.save()
        messages.success(request, f"Loan for {loan.name} has been approved.")
    return redirect(reverse('loan_to_be_approved'))


def approve_savings_account(request, request_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        account = get_object_or_404(Savings, id=request_id)
        action = request.POST.get('action')

        if action == 'approve':
            # Generate a unique account number
            while True:
                if user_id:
                    account_number = f"NWB{random.randint(100000, 999999)}00{user_id}"
                else:
                    account_number = f"NWB{random.randint(10000000, 99999999)}"
                if not Savings.objects.filter(account_number=account_number).exists():
                    break

            account.account_number = account_number
            account.status = "approve"
            account.is_approved = True
            account.is_active = True
            account.save()

            request.session['account_number'] = account_number

        elif action == 'reject':
            account.status = "reject"
            account.is_approved = False
            account.save()

    return redirect('savings_account_approval')


def approve_customer_account(request, account_id):
    if request.method == 'POST':
        account = get_object_or_404(Customer, id=account_id)
        account.is_active = True
        account.save()
        return redirect('savings_account_approval')


def current_account_approval(request):
    pending_accounts = Current.objects.filter(is_active=False)

    context = {
        'pending_accounts': pending_accounts,
    }

    return render(request, 'current_account_approval.html', context)


def approve_current_account(request, account_id):
    if request.method == 'POST':
        account = get_object_or_404(Current, id=account_id)
        action = request.POST.get('action')

        if action == 'approve':
            # Generate a unique account number
            while True:
                if account.user_id:
                    account_number = f"NWB{random.randint(1000000, 9999999)}00{account.user_id}"
                    print(account_number)
                else:
                    account_number = f"NWB{random.randint(1000000, 9999999)}"
                if not Savings.objects.filter(account_number=account_number).exists():
                    break

            account.account_number = account_number
            account.status = "approve"
            account.is_approved = True
            account.is_active = True
            account.save()

            request.session['account_number'] = account_number

        elif action == 'reject':
            account.status = "reject"
            account.is_approved = False
            account.save()

        return redirect('current_account_approval')


# Current account application- email verification
verification_codes = {}


def send_verificationcurrent_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Generate a random 6-digit code
            code = str(random.randint(100000, 999999))
            verification_codes[email] = code

            # Send email with verification code
            subject = 'NanoWealthBank - Email Verification'
            message = f'Your verification code is: {code}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                return JsonResponse({'success': True, 'message': 'Verification code sent successfully'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        else:
            return JsonResponse({'success': False, 'message': 'Email is required'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def currentcode_verify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        if email and code:
            stored_code = verification_codes.get(email)
            if stored_code and stored_code == code:
                # Remove the used code
                del verification_codes[email]
                return JsonResponse({'success': True, 'message': 'Verification successful'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid verification code'})
        else:
            return JsonResponse({'success': False, 'message': 'Email and code are required'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def personal_loan(request):
    user_id = request.session.get('user_id')
    ongoing_loans = LoanApplication.objects.filter(customer=user_id)
    return render(request, 'customer/personal_loan.html', {'ongoing_loans': ongoing_loans})


def loan_application(request):
    if request.method == 'POST':
        try:
            customer = Customer.objects.get(id=request.session.get('user_id'))
            
            # Extract data from the request
            applicant_name = request.POST.get('applicantName')
            nationality = request.POST.get('nationality')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pin_code = request.POST.get('pinCode')
            employment_status = request.POST.get('employmentStatus')
            monthly_income = request.POST.get('monthlyIncome')
            loan_type = request.POST.get('loanType')
            loan_amount = request.POST.get('loanAmount')
            loan_purpose = request.POST.get('loanPurpose')

            # Validate required fields
            if not all([applicant_name, nationality, gender, address, city, state, 
                       pin_code, employment_status, monthly_income, loan_type, 
                       loan_amount, loan_purpose]):
                messages.error(request, 'All fields are required.')
                return redirect('loan_application')

            # Create loan application
            new_loan = LoanApplication.objects.create(
                customer=customer,
                name=applicant_name,
                nationality=nationality,
                gender=gender,
                address=address,
                city=city,
                state=state,
                pin_code=pin_code,
                employment_status=employment_status,
                monthly_income=monthly_income,
                loan_type=loan_type,
                loan_amount_required=loan_amount,
                loan_purpose=loan_purpose,
                application_date=timezone.now(),
                status='PENDING'
            )
            
            # Set next payment date
            next_payment_date = new_loan.application_date + timedelta(days=30)
            new_loan.next_payment_date = next_payment_date
            new_loan.save()
            
            messages.success(request, 'Loan application submitted successfully!')
            return redirect('userdashboard')
            
        except Customer.DoesNotExist:
            messages.error(request, 'Please log in to submit a loan application.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('loan_application')

    return render(request, 'customer/loan_application.html')


# logout
def logout_view(request):
    request.session.flush()
    # Ensure 'login' matches the name in your URLs
    return redirect('login')


def transactions_view(request):
    user = request.user
    user_id = request.session.get('user_id')
    customer = Customer.objects.get(id=user_id)

    if request.method == 'POST':
        if 'deposit-amount' in request.POST:
            # Process deposit
            deposit_amount = Decimal(request.POST.get('deposit-amount'))
            if deposit_amount >= 1000:
                customer.balance += deposit_amount
                customer.save()

                Transaction.objects.create(
                    customer=customer,
                    transaction_type='deposit',
                    amount=deposit_amount
                )

                messages.success(request, f'Amount ₹{
                                 deposit_amount} has been deposited successfully!')
            else:
                messages.error(
                    request, 'Deposit amount must be at least ₹1000.')

        elif 'transfer-amount' in request.POST:
            # Process transfer
            transfer_amount = Decimal(request.POST.get('transfer-amount'))
            recipient_name = request.POST.get('account-holder-name')
            recipient_account = request.POST.get('account-number')
            purpose = request.POST.get('transfer-purpose')

            if transfer_amount >= 1000:
                if customer.balance >= transfer_amount:
                    customer.balance -= transfer_amount
                    customer.save()

                    Transaction.objects.create(
                        customer=customer,
                        transaction_type='transfer',
                        amount=transfer_amount,
                        recipient_name=recipient_name,
                        recipient_account=recipient_account,
                        purpose=purpose
                    )

                    messages.success(request, f'Amount ₹{
                                     transfer_amount} has been transferred successfully!')
                else:
                    messages.error(
                        request, 'Insufficient balance for the transfer!')
            else:
                messages.error(
                    request, 'Transfer amount must be at least ₹1000.')

    # Fetch transactions for the current user
    transactions = Transaction.objects.filter(
        customer=customer).order_by('-timestamp')

    context = {
        # 'account_number': customer.account_number,
        'balance': customer.balance,
        'transactions': transactions,
    }
    return render(request, 'transactions.html', context)


def account_approval_view(request):
    # Fetch all pending savings account requests
    pending_requests = Savings.objects.filter(is_active=0)
    return render(request, 'admin_dashboard.html', {'pending_requests': pending_requests})

# Current Account



# Account approval and verification


def account_approval(request):
    # Fetch data related to customer account approval here
    pending_accounts = Customer.objects.filter(
        status='pending')  # Example query

    context = {
        'pending_accounts': pending_accounts,
    }

    return render(request, 'account_approval.html', context)


def current_interest(request):
    return render(request, 'current_interest.html')

def transfer_receipt(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    context = {
        'receiver_name': transaction.receiver_name,
        'receiver_account_type': transaction.get_receiver_account_type_display(),
        'amount': transaction.amount,
        'date_time': transaction.created_at,
    }
    return render(request, 'transfer_receipt.html', context)

def process_payment(request, transaction_id):
    # Simulate payment logic
    transaction = get_object_or_404(Transaction, id=transaction_id)

    # Simulate payment success (replace this with actual payment gateway logic)
    payment_success = True  # Replace with actual success response from your payment gateway
    
    if payment_success:
        # Mark the transaction as approved
        transaction.is_approved = True
        transaction.save()

        # Redirect to the transfer receipt page
        return redirect('transfer_receipt', transaction_id=transaction.id)
    else:
        # Handle payment failure (optional)
        return HttpResponse("Payment failed. Please try again.")
    



#Apply for card

def apply_card(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login to access this page')
        return redirect('login')
    return render(request, 'customer/apply_card.html')


def classic_card_details(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login to access this page')
        return redirect('login')
    try:
        return render(request, 'customer/classic_card_details.html')
    except Exception as e:
        print(f"Error: {e}")  
        return render(request, 'customer/error.html', {'error': str(e)})

def apply_classic_card(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login to access this page')
        return redirect('login')
    
    user_id = request.session.get('user_id')
    customer = Customer.objects.get(id=user_id)
    print("customer",customer.email)
    if request.method == 'POST':
        try:
            # Create new application
            application = ClassicCardApplication(
                customer_id=user_id,
                full_name=customer.customer_name,
                email=customer.email,
                mobile=customer.mobile_number,
                date_of_birth=customer.date_of_birth,
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                pincode=request.POST.get('pincode')
            )
            print("application",application)  
            application.save()
            
            # Send email to customer
            subject = 'Classic Card Application Received - NanoWealth Bank'
            message = f"""Dear {customer.customer_name},

Thank you for applying for the NanoWealth Bank Classic Card.

Your application has been received and is currently under review. Upon approval, your card will be delivered to your registered address within 7-10 business days.

Application Details:
- Card Type: Classic Card
- Delivery Address: {request.POST.get('address')}, {request.POST.get('city')}, {request.POST.get('state')} - {request.POST.get('pincode')}

We will notify you once your card is dispatched.

Best Regards,
Team NanoWealth Bank"""

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [customer.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error sending email: {e}")
            
            messages.success(request, 'Your Classic Card application has been submitted successfully! Please check your email for confirmation.')
            return redirect('userdashboard')
            
        except Exception as e:
            messages.error(request, 'There was an error submitting your application. Please try again.')
            print(f"Error saving application: {e}")
    
    context = {
        'customer': customer
    }
    return render(request, 'customer/apply_classic_form.html', context)

def admin_card_applications(request):
    applications = ClassicCardApplication.objects.all().order_by('-application_date')
    print("applications requests",applications)
    return render(request, 'admin/card_applications.html', {'applications': applications})

def approve_classiccard_application(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(ClassicCardApplication, id=application_id)
        application.status = 'approved'
        application.save()

        # Prepare email
        subject = 'Your Credit Card Application has been Approved!'
        
        # Context for email template
        context = {
            'name': application.full_name,
            'card_type': 'Classic Card',
        }
        
        # Render HTML email template
        html_content = render_to_string('admin/card_approval_email.html', context)
        
        # Create email message
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[application.email]
        )
        
        # Set email content type to HTML
        email.content_subtype = "html"
        
        # Updated path to card image
        card_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'classic_card.jpg')
        
        # Attach card image if it exists
        if os.path.exists(card_image_path):
            with open(card_image_path, 'rb') as f:
                email.attach('classic_card.png', f.read(), 'image/png')
        else:
            print(f"Card image not found at: {card_image_path}")
        
        # Send email
        try:
            email.send()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {str(e)}")

        return redirect('admin_card_applications')
    return redirect('admin_card_applications')

def reject_classiccard_application(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(ClassicCardApplication, id=application_id)
        application.status = 'rejected'
        application.save()
    return redirect('admin_card_applications')

def block_classiccard_application(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(ClassicCardApplication, id=application_id)
        application.status = 'blocked'
        application.save()
    return redirect('admin_card_applications')


#admin- manager
def manager_list(request):
    managers = Manager.objects.all()
    return render(request, 'manager_list.html', {'managers': managers})

def generate_password():
    # Generate a random 8-character password
    characters = string.ascii_letters + string.digits + "@#$%^&*"
    return ''.join(random.choices(characters, k=8))

def add_manager(request):
    if request.method == 'POST':
        try:
            # Generate password
            password = generate_password()
            
            # Create manager instance
            manager = Manager(
                name=request.POST['name'],
                branch=request.POST['branch'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                status=request.POST['status'],
                password=make_password(password)  # Hash the password
            )
            
            # Save manager (this will trigger the save method that generates manager_id)
            manager.save()

            # Send email with credentials
            subject = 'Your Manager Account Credentials'
            message = f"""
            Dear {manager.name},

            Your manager account has been created successfully. Here are your login credentials:

            Manager ID: {manager.manager_id}
            Password: {password}

            Please change your password after your first login.

            Best regards,
            NanoWealth Bank Team
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    'noreply@nanowealthbank.com',  # Replace with your email
                    [manager.email],
                    fail_silently=False,
                )
                messages.success(request, 'Manager added successfully! Credentials have been sent to their email.')
            except Exception as e:
                messages.warning(request, 'Manager added successfully but failed to send email. Please provide credentials manually.')
            
            return redirect('manager_list')

        except Exception as e:
            messages.error(request, f'Error adding manager: {str(e)}')
            return render(request, 'add_manager.html')
    
    return render(request, 'manager/add_manager.html')

def edit_manager(request, manager_id):
    manager = get_object_or_404(Manager, id=manager_id)
    if request.method == 'POST':
        try:
            # Update manager details
            manager.name = request.POST['name']
            manager.branch = request.POST['branch']
            manager.email = request.POST['email']
            manager.phone = request.POST['phone']
            manager.status = request.POST['status']
            manager.save()
            messages.success(request, 'Manager updated successfully!')
            return redirect('manager_list')
        except Exception as e:
            messages.error(request, f'Error updating manager: {str(e)}')
    return render(request, 'edit_manager.html', {'manager': manager})

def view_manager(request, manager_id):
    manager = get_object_or_404(Manager, id=manager_id)
    return render(request, 'view_manager.html', {'manager': manager})

def managerdashboard(request):
    # # Check if user is logged in via session
    # if not request.session.get('user_id'):
    #     messages.error(request, "Please login first")
    #     return redirect('login')
    # 
    # if request.session.get('user_role') != 'manager':
    #     messages.error(request, "Unauthorized access")
    #     return redirect('login')
    # 
    # try:
    #     manager_id = request.session.get('user_id')
    #     manager = Manager.objects.get(id=manager_id)
    #     
    #     context = {
    #         'manager': manager,
    #         'username': request.session.get('username'),
    #         'manager_id': request.session.get('manager_id')
    #     }
    #     
    #     return render(request, 'manager/manager_dashboard.html', context)
    #     
    # except Manager.DoesNotExist:
    #     messages.error(request, "Manager not found")
    #     return redirect('login')
    # except Exception as e:
    #     messages.error(request, f"An error occurred: {str(e)}")
    #     return redirect('login')


    return render(request, 'manager/manager_dashboard.html')

#card activation email otp
def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
    subject = 'NanoWealth Bank - Card Activation OTP'
    message = f'''
    Dear Customer,

    Your OTP for card activation is: {otp}

    This OTP is valid for a limited time. Please do not share this OTP with anyone.

    Best Regards,
    NanoWealth Bank Team
    '''
    
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def activate_classiccard(request):
    if request.method == 'POST':
        try:
            customer = Customer.objects.get(id=request.session.get('user_id'))
            
            # Get form data
            card_number = request.POST.get('card_number')
            
            # Basic validation
            if not card_number or len(card_number) != 16:
                messages.error(request, 'Please enter a valid 16-digit card number.')
                return render(request, 'customer/activate_classiccard.html', {'customer': customer})
            
            # Generate OTP
            otp = generate_otp()
            
            # Send OTP via email
            if send_otp_email(customer.email, otp):
                # Store in session for verification
                request.session['card_number'] = card_number
                request.session['card_activation_otp'] = otp
                request.session['otp_timestamp'] = str(timezone.now())
                
                messages.success(request, f'OTP has been sent to your email address: {customer.email}')
                return redirect('enter_otp')  # Redirect to new OTP entry page
            else:
                messages.error(request, 'Failed to send OTP. Please try again.')
                return render(request, 'customer/activate_classiccard.html', {'customer': customer})
                
        except Customer.DoesNotExist:
            messages.error(request, 'Customer not found.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'customer/activate_classiccard.html')
    
    # GET request
    try:
        customer = Customer.objects.get(id=request.session.get('user_id'))
        return render(request, 'customer/activate_classiccard.html', {'customer': customer})
    except Customer.DoesNotExist:
        messages.error(request, 'Please login to activate your card.')
        return redirect('login')

def enter_otp(request):
    if request.method == 'POST':
        try:
            customer = Customer.objects.get(id=request.session.get('user_id'))
            entered_otp = request.POST.get('otp')
            stored_otp = request.session.get('card_activation_otp')
            card_number = request.session.get('card_number')
            
            if not stored_otp:
                messages.error(request, 'OTP expired. Please request a new one.')
                return redirect('activate_classic_card')
            
            if entered_otp == stored_otp:
                # Update customer details
                customer.card_number = card_number
                customer.is_card_active = True
                customer.card_activation_date = timezone.now()
                customer.save()
                
                # Clear session data
                session_keys = ['card_activation_otp', 'otp_timestamp', 'card_number']
                for key in session_keys:
                    if key in request.session:
                        del request.session[key]
                
                messages.success(request, 'Your classic card has been activated successfully!')
                return redirect('userdashboard')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
                return render(request, 'customer/enter_otp.html', {'customer': customer})
        
        except Customer.DoesNotExist:
            messages.error(request, 'Customer not found.')
            return redirect('login')
    
    # GET request
    try:
        customer = Customer.objects.get(id=request.session.get('user_id'))
        if not request.session.get('card_activation_otp'):
            messages.error(request, 'Please request OTP first.')
            return redirect('activate_classic_card')
        return render(request, 'customer/enter_otp.html', {'customer': customer})
    except Customer.DoesNotExist:
        messages.error(request, 'Please login to continue.')
        return redirect('login')


#credit score
def check_loan_eligibility(request):
    if request.method == 'POST':
        customer = request.user.customer
        
        # Get or create credit score
        credit_score, created = CreditScore.objects.get_or_create(customer=customer)
        credit_score.update_credit_score()
        
        loan_amount = float(request.POST.get('loan_amount'))
        
        context = {
            'credit_score': credit_score.score,
            'credit_rating': credit_score.get_credit_rating(),
            'payment_history': credit_score.payment_history,
            'credit_utilization': credit_score.credit_utilization,
            'income_factor': credit_score.income_factor,
            'employment_factor': credit_score.employment_factor,
            'age_factor': credit_score.age_factor,
            'is_eligible': credit_score.score >= 650  # Minimum score for loan approval
        }
        
        return render(request, 'customer/loan_eligibility.html', context)
    
    return render(request, 'customer/loan_application.html')


#chatbot
@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        # Configure Gemini API
        genai.configure(api_key='AIzaSyCxaJdu6UNroGJyPE92K0efhJ4eCPHsK7E')
        model = genai.GenerativeModel('gemini-pro')

        try:
            # Get response from Gemini
            response = model.generate_content(user_message)
            return JsonResponse({'response': response.text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def extract_content_from_template(template_name):
    try:
        template_path = os.path.join(settings.BASE_DIR, 'templates', template_name)
        with open(template_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading template {template_name}: {e}")
        return ""

def get_site_content(request):
    site_content = {
        'pages': {
            'accounts': extract_content_from_template('accounts.html'),
            'services': extract_content_from_template('services.html'),
            'about': extract_content_from_template('about.html'),
            'contact': extract_content_from_template('contact.html')
        },
        'faqs': extract_faqs(),
        'products': get_product_information()
    }
    
    return JsonResponse(site_content)

from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
import google.ai.generativelanguage as glm
import google.generativeai as genai

def is_banking_related(query):
    banking_keywords = [
        'loan', 'account', 'deposit', 'credit', 'debit', 'transfer', 'balance',
        'interest', 'bank', 'transaction', 'atm', 'card', 'savings', 'current',
        'fixed deposit', 'fd', 'kyc', 'upi', 'neft', 'rtgs', 'imps', 'branch',
        'payment', 'emi', 'insurance', 'investment', 'mutual fund'
    ]
    return any(keyword in query.lower() for keyword in banking_keywords)

def chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if not is_banking_related(user_message):
            return JsonResponse({
                'response': "I can only assist with banking-related queries. Please ask questions about our banking services."
            })

        # Configure Gemini
        genai.configure(api_key='AIzaSyCxaJdu6UNroGJyPE92K0efhJ4eCPHsK7E')
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"As a bank assistant, answer this query: {user_message}"
        response = model.generate_content(prompt)
        
        return JsonResponse({
            'response': response.text
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)

#salary certificate upload
@ensure_csrf_cookie
def upload_salary_certificate(request):
    if request.method == 'POST' and request.FILES.get('salaryCertificate'):
        try:
            file = request.FILES['salaryCertificate']
            
            # Validate file type
            if not file.content_type == 'application/pdf':
                return JsonResponse({'error': 'Please upload a PDF file only'}, status=400)
            
            # Validate file size (5MB)
            if file.size > 5 * 1024 * 1024:
                return JsonResponse({'error': 'File size should not exceed 5MB'}, status=400)
            
            # Save file
            fs = FileSystemStorage()
            filename = fs.save(f'salary_certificates/{file.name}', file)
            file_url = fs.url(filename)
            
            return JsonResponse({
                'success': True,
                'message': 'File uploaded successfully',
                'file_url': file_url
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request'
    }, status=400)

#download receipt after payment success in internet banking
@require_POST
def download_receipt(request):
    # Get data from POST request
    payment_id = request.POST.get('payment_id')
    receiver_name = request.POST.get('receiver_name')
    receiver_account = request.POST.get('receiver_account_number')
    amount = request.POST.get('amount')
    transaction_date = request.POST.get('transaction_date')
    
    # Create the HttpResponse object with PDF headers
    buffer = BytesIO()
    
    # Create the PDF object using ReportLab
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    ))
    
    # Add the "Payment Receipt" title
    elements.append(Paragraph("Payment Receipt", styles['CustomTitle']))
    elements.append(Spacer(1, 12))
    
    # Create the table data
    data = [
        ['Payment ID:', payment_id],
        ['Beneficiary Name:', receiver_name],
        ['Account Number:', receiver_account],
        ['Amount:', f'₹{amount}'],
        ['Transaction Date:', transaction_date],
    ]
    
    # Create table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
    ])
    
    # Create the table and apply the style
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(table_style)
    
    elements.append(table)
    
    # Build the PDF document
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and return the PDF as a response
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payment_receipt_{payment_id}.pdf"'
    response.write(pdf)
    
    return response



