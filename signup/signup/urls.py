from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage,name="homepage"),
    path('signup/',views.SignupView.as_view(),name="signuppage"),
    path('login',views.loginpage,name="loginpage"),
    path('welcome',views.welcomepage,name="welcomepage"),
    path('logout',views.logoutpage,name='logoutpage'),
    path('activate/<uidb64>/<token>',views.activate,name="activate")
]
