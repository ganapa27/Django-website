from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
from .form import *
from django.contrib import messages
from . import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import generate_token

# def signuppage(request):
#     if request.method == "POST":
#         if request.POST.get('password1') == request.POST.get('password2'):
#             try:
#                 saveuser = User.objects.create_user(request.POST.get('username'),password = request.POST.get('password1'))
#                 saveuser.save()
#                 return render(request,'signup.html',{'form':UserCreationForm(),'info:':'The user' + request.POST.get('username') + 'is saved...!!'})
#             except IntegrityError:
#                 return render(request,'signup.html',{'form':UserCreationForm(),'error:':'The user' + request.POST.get('username') + 'already exists..!!'})
#         else:
#             return render(request,'signup.html',{'form':UserCreationForm(),'error':'The passwords are not matching...!!'})
#     else:
#         return render(request,'signup.html',{'form':UserCreationForm()})

def loginpage(request):
    if request.method == "POST":
        logincorrect = authenticate(request,username=request.POST.get('username'),password=request.POST.get('password'))
        if logincorrect is None:
            return render(request,'login.html',{'form':AuthenticationForm(),'error':'The username or password is wrong...!!'})
        else:
            messages.success(request, "Login Successful!!")
            login(request,logincorrect)
            return redirect('welcomepage')
    else:
        return render(request,'login.html',{'form':AuthenticationForm()})

def welcomepage(request):
    return render(request,'welcome.html')

def logoutpage(request):
    if request.method=="POST":
        messages.success(request, "Logout Successful!!")
        logout(request)
    return redirect('signuppage')

class SignupView(View):
    def get(self, request):
        # fm = UserCreationForm()
        fm = SignupForm()
        return render(request,'signup.html', {'form':fm})
    def post(self,request):
        username = request.POST['username']
        email = request.POST['email']
        fm = SignupForm(request.POST)
        user = User.objects.create_user(username = username,email = email)
        email_subject = 'Activate your account'
        email_body = 'Hello' + user.username + ''
        if fm.is_valid():
            messages.success(request, "Registration Successful, we have sent you a confirmation email, please confirm your email in order to activate your account")

            fm.save()

            user.is_active = False
            email = EmailMessage(
                email_subject,
                email_body,
                'rakshithg2000@gmail.com',
                [user.email],
            )

            # Welcome Email

            subject = "Welcome to our website!!"
            message = "Hello " + user.username + "!!\n" + "Welcome!!\n Thank You for visitng our website\n We have also sent you a confirmation email, please confirm email address in order to activate your account. \n\n Thanking You"
            from_email = settings.EMAIL_HOST_USER

            to_list = [user.email]
            send_mail(subject,message,from_email,to_list,fail_silently=True)

            # Email Confirmation

            current_site = get_current_site(request)
            email_subject = "Confirm your email !!"
            email_message = render_to_string('email_confirmation.html',{
                'name': username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            email = EmailMessage(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = True
            email.send()

            return redirect('signup/')
            
        else:
            return render(request,'signup.html', {'form':fm})


def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user,token):
        user.is_active = True
        user.save()
        login(request,user)
        return redirect('')
    else:
        return redirect(request,'activation_failed.html')


def homepage(request):
    return render(request, 'home.html') 
