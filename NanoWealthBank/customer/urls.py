from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.shortcuts import redirect

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', views.accounts, name='accounts'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),  # Ensure this matches your custom login view
    path('userdashboard/', views.dashboard, name='userdashboard'),

    path('personal_banking/', views.personal_banking, name='personal_banking'),
    path('business_banking/', views.business_banking, name='business_banking'),
    path('signup/', views.signup, name='signup'),

    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Forgot password view
    path('forgot_password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('verifycode/<str:email>/',views.verifycode,name="verify_code"),
]
