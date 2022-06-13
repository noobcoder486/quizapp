from django.urls import path
from . views import QuestionView, ScoreListView, TopicView


urlpatterns = [
    path('', TopicView.as_view(), name='topic'),
    path('<uuid:topic_id>', QuestionView.as_view(), name='quiz'),
    path('score/<uuid:topic_id>/', ScoreListView.as_view(), name='score'),
]