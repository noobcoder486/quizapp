from django.urls import path
from .import views
from .views import ScoreListView, TopicView


urlpatterns = [
    path('', TopicView.as_view(), name='topic'),
    path('<t_id>', views.nextques, name='quiz'),
    path('score/<t_id>/', ScoreListView.as_view(), name='score'),
]