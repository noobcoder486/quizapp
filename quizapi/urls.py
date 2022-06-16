from django.urls import path
from .views import QuestionAPIView, ResendOtpAPIView, ResultAPIView, ScoreAPIView, TopicAPIView, UserCreateAPIView, ValidateAPIView

urlpatterns = [
  path('register/',UserCreateAPIView.as_view(), name='register'),
  path('topic/', TopicAPIView.as_view(), name= 'topics'),
  path('<uuid:topic_id>', QuestionAPIView.as_view(), name='question'),
  path('validate_otp', ValidateAPIView.as_view(), name='validate'),
  path('resend_otp', ResendOtpAPIView.as_view(), name="resend_otp"),
  path("result/<uuid:topic_id>", ResultAPIView.as_view(), name = "result"),
  path('score/<uuid:topic_id>', ScoreAPIView.as_view(), name='score')
]