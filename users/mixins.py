import imp
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.contrib import messages

class UserVerifiedMixin(AccessMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.email_confirmed == False:
            messages.warning(request, f"Please Enter the OTP sent on the Email")
            return HttpResponseRedirect(reverse('validate', kwargs={"user":request.user}))
        return super().dispatch(request, *args, **kwargs)