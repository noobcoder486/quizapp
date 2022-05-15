from django.urls import path
from .import views
from .views import TopicView #QuestionListView,


urlpatterns = [
    path('', TopicView.as_view(), name='topic'),
    path('<t_id>', views.nextques, name='quiz'),
    path('savedata', views.savedata, name='save-data')
]