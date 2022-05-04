from django.urls import path
from .views import DataListView, SubjectView, TopicView


urlpatterns = [
    path('', SubjectView.as_view(), name='home'),
    path('<id>', TopicView.as_view(), name='topic'),
    path('<s_id>/<t_id>', DataListView.as_view(), name='quiz')
]

