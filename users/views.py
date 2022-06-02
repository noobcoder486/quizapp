import pyotp
from . models import CustomUser
from .forms import UserRegisterForm
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user=CustomUser.objects.get(username=username)
            email=form.cleaned_data.get('email')
            otp=pyotp.TOTP(user.secret_key, interval=300)
            user=CustomUser.objects.get(username=username)
            send_mail(
                'Sign Up One Time Password',
                otp.now(),
                'dubeyshubham823@yahoo.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, f'Account Created for {username}. Please Enter the Otp you recieved on your mail id')
            return HttpResponseRedirect(reverse('validate', kwargs={'user':username}))
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form},)


def validate(request,user):
    if request.method=="POST":
        user_object=CustomUser.objects.get(username=user)
        secret_key=user_object.secret_key
        generated_otp=pyotp.TOTP(secret_key, interval=300)
        sent_otp=generated_otp.now()
        print(sent_otp)
        user_otp=request.POST.get("otp")
        print(user_otp)
        x=generated_otp.verify(user_otp)
        if x is True:
            user_object.email_confirmed=True
            user_object.save()
            messages.success(request, f'OTP validation successfull for {user}. You can Login')
            return redirect('login')
        else:
            messages.error(request, f'OTP validation was failed for {user}. You can Login')
            return HttpResponseRedirect(reverse('validate', kwargs={'user':user}))
    else:
        return render(request, "users/validate.html")