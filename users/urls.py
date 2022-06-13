from django.contrib.auth import views as auth_views
from django.urls import path
from . import views as user_views


urlpatterns=[
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name = 'logout'),
    path('register/', user_views.RegisterView.as_view(), name= 'register'),
    path('resend_otp/', user_views.resend_otp, name="resend_otp"),
    path('validate/', user_views.ValidateView.as_view(), name="validate"),
    
]