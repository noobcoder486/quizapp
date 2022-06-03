import pyotp
from . forms import UserRegisterForm
from . models import CustomUser
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import View

class RegisterView(View):
    template_name = "users/register.html"

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = CustomUser.objects.get(username=username)
            email = form.cleaned_data.get('email')
            otp = pyotp.TOTP(user.secret_key, interval=300)
            user = CustomUser.objects.get(username=username)
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


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             user = CustomUser.objects.get(username=username)
#             email = form.cleaned_data.get('email')
#             otp = pyotp.TOTP(user.secret_key, interval=300)
#             user = CustomUser.objects.get(username=username)
#             send_mail(
#                 'Sign Up One Time Password',
#                 otp.now(),
#                 'dubeyshubham823@yahoo.com',
#                 [email],
#                 fail_silently = False,
#             )
#             messages.success(request, f'Account Created for {username}. Please Enter the Otp you recieved on your mail id')
#             return HttpResponseRedirect(reverse('validate', kwargs={'user':username}))
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})

class ValidateView(View):
    template_name = "users/validate.html"

    def post(self, request, *args, **kwargs):
        user=self.kwargs.get("user")
        user_object = CustomUser.objects.get(username=user)
        secret_key = user_object.secret_key
        generated_otp = pyotp.TOTP(secret_key, interval=300)
        sent_otp = generated_otp.now()
        print(sent_otp)
        user_otp=request.POST.get("otp")
        print(user_otp)
        x=generated_otp.verify(user_otp)
        if x is True:
            user_object.email_confirmed = True
            user_object.save()
            messages.success(request, f'OTP validation successfull for {user}. You can Login')
            return redirect('login')
        else:
            messages.error(request, f'OTP validation was failed for {user}. You cant Login')
            return HttpResponseRedirect(reverse('validate', kwargs={'user': {user}}))

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)



# def validate(request,user):
#     if request.method=="POST":
#         user_object = CustomUser.objects.get(username=user)
#         secret_key = user_object.secret_key
#         generated_otp = pyotp.TOTP(secret_key, interval=300)
#         sent_otp = generated_otp.now()
#         print(sent_otp)
#         user_otp=request.POST.get("otp")
#         print(user_otp)
#         x=generated_otp.verify(user_otp)
#         if x is True:
#             user_object.email_confirmed = True
#             user_object.save()
#             messages.success(request, f'OTP validation successfull for {user}. You can Login')
#             return redirect('login')
#         else:
#             messages.error(request, f'OTP validation was failed for {user}. You cant Login')
#             return HttpResponseRedirect(reverse('validate', kwargs={'user':user}))
#     else:
#         return render(request, "users/validate.html")