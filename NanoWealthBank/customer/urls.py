from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView
from .views import LogoutView 
from .views import savings_account
from .views import logout_view
from django.urls import path
from .views import logout_view
from .views import account_approval_view, approve_savings_account, reject_savings_account, pending_savings_account


urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', views.accounts, name='accounts'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
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
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_code/<str:email>/', views.verify_code, name='verify_code'),
    path('reset_password/<str:email>/', views.reset_password, name='reset_password'), 
    path('verify_forgotcode/<str:email>/',views.verifyforgotcode,name="verify_forgotcode"),
    path('admin_dashboard/', views.admin_dashboard, name='admindashboard'),
    path('approve/<int:id>/', views.approve_customer, name='approve_customer'),
    path('view/<int:id>/', views.view_customer, name='view_customer'),
    path('edit/<int:id>/', views.edit_customer, name='edit_customer'),
    path('block/<int:id>/', views.block_customer, name='block_customer'),

    path('login/', views.login, name='login'), 
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('savings-account/', views.savings_account, name='savings_account'),
    path('savings-accounts/', views.savings_accounts, name='savings_accounts'),
    path('savings_application/', views.savings_application, name='savings_application'),
    path('submit_registration/', views.submit_registration, name='submit_registration'),

    #path('savings_requests/', views.savings_requests, name='savings_requests'),
    #path('approve_account/<int:account_id>/', views.approve_account, name='approve_account'),
    #path('block_account/<int:account_id>/', views.block_account, name='block_account'),

    path('admin_dashboard/', views.customer_login_requests, name='customer_login_requests'),
    path('approve_customer/<int:customer_id>/', views.approve_customer, name='approve_customer'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('block_customer/<int:customer_id>/', views.block_customer, name='block_customer'),

    # path('account-approval/', views.account_approval_view, name='account_approval'),
    path('savings_interest/', views.savings_interest, name='savings_interest'),
    
    path('logout_view/', views.logout_view, name='logout_view'),


    path('transactions/', views.transactions_view, name='transactions_view'),
    path('transactions/', views.transactions, name='transactions'),
    
    path('admin/account-approval/', views.account_approval_view, name='account_approval'),
    path('admin/approve-savings-account/<int:request_id>/', approve_savings_account, name='approve_savings_account'),
    path('admin/reject-savings-account/<int:request_id>/', reject_savings_account, name='reject_savings_account'),
    path('admin/pending-savings-account/<int:request_id>/', pending_savings_account, name='pending_savings_account'),

     #View Profile
     path('profile/', views.view_profile, name='view_profile'),

     #Current account
     path('current_account/', views.current_account, name='current_account'),

    #customer login requests- admin dashboard
    path('customer-requests/', views.customer_login_requests, name='customer_login_requests'),
     
]

