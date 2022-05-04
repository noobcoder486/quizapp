from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Subject, Topic, Question, Answer
from django.utils.decorators import method_decorator
from django.shortcuts import render

@method_decorator(login_required, name='dispatch')
class SubjectView(ListView):
    model = Subject
    template_name = 'quiz/home.html'
    context_object_name= 'subjects'

class TopicView(ListView):
    model = Topic
    template_name = 'quiz/topic.html'
    context_object_name = 'topics'

    def get_queryset(self):
        id = self.kwargs.get('id')
        queryset= Topic.objects.filter(subject=id)
        return queryset

class DataListView(ListView):
    model = Question
    template_name = 'quiz/quizz.html'
    context_object_name = 'questions'

    def get_queryset(self):
        pkey=self.kwargs.get('t_id')
        queryset= Question.objects.filter(topic=pkey)
        return queryset

