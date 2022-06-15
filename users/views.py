from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from . forms import UserRegisterForm, ValidateForm


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy('topic')

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        user.send_otp()
        messages.success(self.request, f"Account Successfully Created for {username}.")
        return super().form_valid(form)



class ValidateView(FormView):
    template_name = "users/validate.html"
    form_class = ValidateForm
    success_url = reverse_lazy('topic')

    def form_valid(self, form):
        otp = form.cleaned_data["otp"]
        user = self.request.user
        if user.email_confirmed:
            messages.info(self.request, f"User is already validated!")
        else:
            verify_otp = user.verify_otp(otp)
            if verify_otp:
                messages.success(self.request, f'OTP validation successfull for {user}')
            else:
                messages.warning(self.request, f"OTP is Incorrect")
                return super().form_invalid(form)
        return super().form_valid(form)
    
def resend_otp(request):
        user = request.user
        user.send_otp()
        messages.success(request, f'Otp Sent Successful for {user}. Please Enter the Otp you recieved on your mail id')
        return redirect('validate')