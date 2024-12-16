from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import approve_savings_account


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
    path('login/', views.login, name='login'), 
    path('logout_view/', views.logout_view, name='logout_view'),
    
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


    path('view/<int:id>/', views.view_customer, name='view_customer'),
    path('edit/<int:id>/', views.edit_customer, name='edit_customer'),


    # customer
    path('profile/', views.view_profile, name='view_profile'),
    #Savings account 
    path('savings-account/', views.savings_account, name='savings_account'),
    path('savings-application/', views.savings_application, name='savings_application'),
    path('savings-account/apply/', views.savings_application, name='savings_application'),
    path('send-verification-code/', views.send_verification_code, name='send_verification_code'),
    path('code-verify/', views.code_verify, name='code_verify'),
    path('submit-application/', views.submit_application, name='submit_application'),
    path('current_account/', views.current_account, name='current_account'),
    path('current_application/', views.current_application, name='current_application'),
     path('submit-application-current/', views.submit_application_current, name='submit_application_current'),
    path('topup/', views.topup_balance, name='topup_balance'),

    #Personal loan
    path('personal_loan/', views.personal_loan, name='personal_loan'),
    path('loan_application/', views.loan_application, name='loan_application'),

    # transcations
    path('transactions/', views.transactions, name='transactions'),
    path('list_deposits/', views.list_deposits, name='list_deposits'),
    path('add_deposit/', views.add_deposit, name='add_deposit'),
    path('download_statement/', views.download_statement, name='download_statement'),
    path('internet_banking/', views.internet_banking, name='internet_banking'),

    path('admin_dashboard/', views.admin_dashboard, name='admindashboard'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('approve_customer/<int:customer_id>/', views.approve_customer, name='approve_customer'),
    path('block_customer/<int:customer_id>/', views.block_customer, name='block_customer'),
    path('loanofficer_list/', views.loanofficer_list, name='loanofficer_list'),
    path('add_loanOfficer_user/', views.add_loanOfficer_user, name='add_loanOfficer_user'),
    path('loan_list/', views.loan_list, name='loan_list'),
    path('loan_status_toggle/<int:loan_id>', views.loan_status_toggle, name='loan_status_toggle'),
    path('transactions_list/', views.transactions_list, name='transactions_list'),
    path('transaction_cancel_or_approve/<int:transaction_id>/', views.transaction_cancel_or_approve, name='transaction_cancel_or_approve'),
    path('savings-account-approval/', views.savings_account_approval, name='savings_account_approval'),
    path('admin-dashboard/approve-savings-account/<int:request_id>/', approve_savings_account, name='approve_savings_account'),
    path('current-account-approval/', views.current_account_approval, name='current_account_approval'),
    path('approve-current-account/<int:account_id>/', views.approve_current_account, name='approve_current_account'),
    


    # path('account-approval/', views.account_approval_view, name='account_approval'),
    path('loanofficerdashboard/', views.loanofficerdashboard, name='loanofficerdashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('loan_to_be_approved/', views.loan_to_be_approved, name='loan_to_be_approved'),
    path('loans/approve/<int:loan_id>/', views.approve_loan, name='approve_loan'),

    path('transactions/', views.transactions_view, name='transactions_view'),
    
    # Admin sections
    path('admin/account-approval/', views.account_approval_view, name='account_approval'),

     #View Profile

     #Current account



   


    #Current account application
    path('current_interest/', views .current_interest, name='current_interest'),

   

    #Admin- savings approval and verification    
    path('approve-customer-account/<int:account_id>/', views.approve_customer_account, name='approve_customer_account'),
    

    #Admin- current approval and verification   
    # 

#razorpay
path('internet_banking/', views.internet_banking, name='internet_banking'),

#path('send-money/', views.send_money, name='send_money'),
#path('process-payment/', views.process_payment, name='process_payment'),
#path('payment-success/', views.payment_success, name='payment_success'), 

]

