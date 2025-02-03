"""
URL configuration for NanoWealthBank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from customer import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customer.urls')),
    path('', views.home, name='home'),
    path('verify/<str:uidb64>/<str:token>/', views.activate, name='activate'),  
    path('userdashboard/', views.dashboard, name='userdashboard'),  
    path('chat/', views.chat_view, name='chat'),
    path('get-site-content/', views.get_site_content, name='get-site-content'),
    path('upload-salary-certificate/', views.upload_salary_certificate, name='upload_salary_certificate'),
    path('download-receipt/', views.download_receipt, name='download_receipt'),
    path('customer/card_details/', views.card_details, name='card_details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







