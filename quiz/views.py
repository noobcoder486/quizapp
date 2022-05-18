from multiprocessing import context
from urllib import request
from django.views import View
from django.views.generic import ListView,View
from django.contrib.auth.decorators import login_required
from .models import Topic, Question, Answer, UserRecord
from django.utils.decorators import method_decorator
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect


@method_decorator(login_required, name='dispatch')
class TopicView(ListView):
    model = Topic
    template_name = 'quiz/topic.html'
    context_object_name = 'topics'

    
def nextques(request,t_id):
    if request.method=="POST":
        user=request.user
        question_id=request.POST.get('hidden1')
        question_object=Question.objects.get(q_id=question_id)     
        question=request.POST.get('hidden')
        answer_id=request.POST.get(question)
        answer_object=Answer.objects.get(a_id=answer_id)
        topic_object=Topic.objects.get(t_id=t_id)
        query=UserRecord(User=user,question=question_object,answer_choosen=answer_object,topic=topic_object)
        query.save()
    questions=Question.objects.filter(topic=t_id)
    total_questions=[]
    for question in questions:
        total_questions.append(str(question.q_id))
    user_answered=UserRecord.objects.filter(User=request.user).filter(topic=t_id)
    answered_list=[]
    for answered_question in user_answered:
        answered_list.append(str(answered_question.question.q_id))
    for question_id in total_questions:
        if question_id not in answered_list:
            questionset=Question.objects.filter(q_id=question_id)
            answerset=Answer.objects.filter(question=question_id)
            break
        else:
            continue
    if len(user_answered)<len(total_questions):
        return render(request, "quiz/quizz.html", context={"questions":questionset,"answers":answerset,})
    else:
        return HttpResponseRedirect(reverse('score', kwargs={"t_id":t_id}))

class ScoreListView(ListView):
    model=UserRecord
    template_name="quiz/quizend.html"
    context_object_name="scores"


    def get_queryset(self):
        topic_id=self.kwargs.get('t_id')
        userrecord=UserRecord.objects.filter(User=self.request.user).filter(topic=topic_id)
        return userrecord
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_id=self.kwargs.get('t_id')
        Userrecord=UserRecord.objects.filter(User=self.request.user).filter(topic=topic_id)
        total_score=0
        for score in Userrecord:
            if score.answer_choosen.is_correct:
                print(score.answer_choosen.is_correct)
                total_score= total_score+1
        self.request.session['score']=total_score
        context['score']=self.request.session['score']
        return context

    





        
        