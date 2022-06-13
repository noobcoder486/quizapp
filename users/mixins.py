import imp
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View


class UserVerifiedMixin(AccessMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.email_confirmed == False:
            messages.warning(request, f"Please Enter the OTP sent on the Email")
            return redirect('validate')
        return super().dispatch(request, *args, **kwargs)