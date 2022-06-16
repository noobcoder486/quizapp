from django.urls import path
from .views import LoginAPIView, LogoutAPIView, QuestionAPIView, ResendOtpAPIView, ResultAPIView, ScoreAPIView, TopicAPIView, UserCreateAPIView, ValidateAPIView

urlpatterns = [
  path('login/', LoginAPIView.as_view(), name="api_login"),
  path('logout/', LogoutAPIView.as_view(), name="api_logout"),
  path('register/',UserCreateAPIView.as_view(), name='api_register'),
  path('resend_otp', ResendOtpAPIView.as_view(), name="api_resend_otp"),
  path("result/<uuid:topic_id>", ResultAPIView.as_view(), name = "api_result"),
  path('score/<uuid:topic_id>', ScoreAPIView.as_view(), name='api_score'),
  path('topic/', TopicAPIView.as_view(), name= 'topics'),
  path('<uuid:topic_id>', QuestionAPIView.as_view(), name='api_question'),
  path('validate_otp', ValidateAPIView.as_view(), name='api_validate'),
]