"""
URL configuration for Pharmas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

from django.conf.urls.static import static
from PharmaH import views

urlpatterns = [
    path('',views.home,name='home'),
    path('SecureEncryptoAdmin/', admin.site.urls),
    path('login/',views.handleLogin,name='login'),
    path('managersignup/',views.managersignup,name='managersignup'),
    path('employeesignup/',views.employeesignup,name='employeesignup'),
    path('ComponentEntry/',views.ComponentEntry,name='ComponentEntry'),
    path('medicines/', views.get_medicines, name='get_medicines'),
    path('administrator/',views.administrator,name='Administrator'),
    path('home/',views.home,name='home'),
    path('managerdashboard/',views.Managerdashboard,name='Managerdashboard'),
    path('Employeedashboard/',views.Employeedashboard,name='Employeedashboard'),
    path('add_component/', views.add_component, name='add_component'),
    path('logout/', views.logout_view, name='logout'),
]
