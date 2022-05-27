import pyotp
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib import messages
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            otp=pyotp.totp('base32secret3232')
            form.save()
            messages.success(request, f'Account Created for {User.username}. You can Login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
