from django.shortcuts import render, redirect
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
from .models import Customer

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

def login(request):  # Renamed from `login` to avoid conflict
    if request.method == 'POST':
        #username = request.POST['username']
        #password = request.POST['password']
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  # Renamed to `auth_login` to avoid conflict
            return redirect(reverse('userdashboard'))  # Redirect to the user dashboard
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')  # Re-render the login page with an error message
            
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
import random;

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        dob = request.POST['dob']
        mobile = request.POST['mobilenum']
        custumername= request.POST.get('customername')
        # Create user but keep it inactive
        user = Customer(username=username, email=email, password=password, is_active=False,customer_name=custumername,mobile_number=mobile,date_of_birth=dob)
        user.save();       
        if user:
            try:
                user = User.objects.get(email=email)
                # Generate a random 4-digit code
                code = random.randint(1000, 9999)
                user_pins[email] = code

                # Send email with the code
                send_mail(
                    'Password Reset Code',
                    f'Your password reset code is {code}.',
                    'admin@yourdomain.com',  # Change to your domain
                    [email],
                    fail_silently=False,
                )
                # Redirect to the verification page
                return redirect('verify_code', email=email)
            except User.DoesNotExist:
                messages.error(request, 'Invalid email address.')
    else:
        return render(request, 'signup.html')

def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = f"{request.scheme}://{request.get_host()}/verify/{uid}/{token}/"
    
    subject = 'Verify your email address'
    message = render_to_string('email_verification.html', {
        'user': user,
        'verification_link': verification_link,
    })
    send_mail(subject, message, 'no-reply@yourdomain.com', [user.email])

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

def user_dashboard_view(request):
    # your view logic here
    return render(request, 'dashboard.html')
 


class ForgotPasswordView(TemplateView):
    template_name = 'forgotpassword.html'

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Add logic to handle password reset here
        return HttpResponse("Password reset link sent to your email.")  # Update this response as needed

    return render(request, 'forgotpassword.html')

def verifycode(request,email):
      if request.method == 'POST':
        entered_code = request.POST.get('pin')
        correct_code = user_pins.get(email)

        if correct_code and str(entered_code) == str(correct_code):
            # Redirect to reset password page
            return redirect('reset_password', email=email)
        else:
            messages.error(request, 'Invalid code. Please try again.')

        return render(request, 'verifycode.html',{'email': email})
