import pyotp
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import FormView
from . forms import UserRegisterForm
from . models import CustomUser

class RegisterView(FormView):
    template_name = "users/register.html"

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.save()
            username = form.cleaned_data.get('username')
            user = CustomUser.objects.get(username=username)
            email = form.cleaned_data.get('email')
            otp = pyotp.TOTP(user.secret_key, interval=300)
            send_mail(
                'Sign Up One Time Password',
                otp.now(),
                'dubeyshubham823@yahoo.com',
                [email],
                fail_silently = False,
            )
            messages.success(request, f'Account Created for {username}. Please Enter the Otp you recieved on your mail id')
            return HttpResponseRedirect(reverse('validate', kwargs={'user':username}))
        else:
            return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, self.template_name, {"form": form})


class ValidateView(FormView):
    template_name = "users/validate.html"


    def post(self, request, *args, **kwargs):
        user=self.kwargs.get("user")
        user_object = CustomUser.objects.get(username=user)
        generated_otp = pyotp.TOTP(user_object.secret_key, interval=300)
        sent_otp = generated_otp.now()
        user_otp=request.POST.get("otp")
        x=generated_otp.verify(user_otp)
        if x is True:
            user_object.email_confirmed = True
            user_object.save()
            messages.success(request, f'OTP validation successfull for {user}')
            return redirect('login')
        else:
            messages.error(request, f'OTP validation was failed for {user}. You cant Login')
            return HttpResponseRedirect(reverse('validate', kwargs={'user': user}))

    def get(self, request, *args, **kwargs):
        user=self.kwargs.get('user')
        context={"user":user}
        return render(request, self.template_name, context=context)
    
def resend_otp(request, user):
        user_object= CustomUser.objects.get(username=user)
        user_email=user_object.email
        otp = pyotp.TOTP(user_object.secret_key, interval=300)
        send_mail(
                'Sign Up One Time Password',
                otp.now(),
                'dubeyshubham823@yahoo.com',
                [user_email],
                fail_silently = False,
            )
        messages.success(request, f'Otp Sent Successful on {user_email}. Please Enter the Otp you recieved on your mail id')
        return HttpResponseRedirect(reverse('validate', kwargs={'user':user}))