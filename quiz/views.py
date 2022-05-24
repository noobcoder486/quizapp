from django.views import View
import datetime
from django.views.generic import ListView,View
from django.contrib.auth.decorators import login_required
from pytz import timezone
from .models import Time_Started, Topic, Question, Answer, UserRecord
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

@method_decorator(login_required, name='dispatch')
class TopicView(ListView):
    model = Topic
    template_name = 'quiz/topic.html'
    context_object_name = 'topics'


class QuestionView(View):
    template_name="quiz/quizz.html"

    def get_context_data(self, **kwargs):
        context={}
        t_id=self.kwargs.get('t_id')
        topic = Topic.objects.get(t_id=t_id)
        time_object=Time_Started.objects.get_or_create(User=self.request.user, topic=topic)
        time_started=time_object[0]
        timer=time_started.starting_time #starting time
        current_time=datetime.datetime.now()
        diff=current_time-timer
        difference_in_seconds=diff.seconds
        difference_in_minutes=difference_in_seconds
        total_time=topic.time_required
        if total_time>difference_in_minutes:
            time_left=int(total_time-difference_in_minutes)
        else:
            time_left=-1
        #getting the question refering topic id
        questions=Question.objects.filter(topic=t_id)
        total_questions=[]
        for question in questions:
            total_questions.append(str(question.q_id))
        user_answered=UserRecord.objects.filter(User=self.request.user).filter(topic=t_id)
        answered_list=[]
        for answered_question in user_answered:
            answered_list.append(str(answered_question.question.q_id))   
        for question_id in total_questions:
            if question_id not in answered_list:
                questionset=Question.objects.filter(q_id=question_id)
                answerset=Answer.objects.filter(question=question_id)
                out_of=len(total_questions)
                current=len(answered_list)+1
                context['questionset']=questionset
                context['answerset']=answerset
                context['out_of']=out_of
                context['current']=current
                context['time_left']=time_left
                break   
            else:
                continue
        return context

    def post(self, request, *args, **kwargs):
        t_id=self.kwargs.get('t_id')
        user=self.request.user
        question_id=self.request.POST.get('hidden1')
        question_object=Question.objects.get(q_id=question_id)     
        question=self.request.POST.get('hidden')
        answer_id=self.request.POST.get(question)
        answer_object=Answer.objects.get(a_id=answer_id)
        topic_object=Topic.objects.get(t_id=t_id)
        query=UserRecord(User=user,question=question_object,answer_choosen=answer_object,topic=topic_object)
        query.save()
        questions=Question.objects.filter(topic=t_id)
        total_questions=[]
        for question in questions:
            total_questions.append(str(question.q_id))
        user_answered=UserRecord.objects.filter(User=self.request.user).filter(topic=t_id)
        answered_list=[]
        for answered_question in user_answered:
            answered_list.append(str(answered_question.question.q_id))
        if len(user_answered)<len(total_questions):
            return HttpResponseRedirect(reverse('quiz',kwargs={'t_id':t_id}))
        else:
            return HttpResponseRedirect(reverse('score', kwargs={"t_id":t_id}))
    
    def get(self, request, *args, **kwargs):
        t_id=self.kwargs.get('t_id')
        questions=Question.objects.filter(topic=t_id)
        total_questions=[]
        for question in questions:
            total_questions.append(str(question.q_id))
        user_answered=UserRecord.objects.filter(User=self.request.user).filter(topic=t_id)
        answered_list=[]
        for answered_question in user_answered:
            answered_list.append(str(answered_question.question.q_id))
        if len(user_answered)<len(total_questions):
            return render(request,self.template_name,self.get_context_data())
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
                total_score= total_score+1
        self.request.session['score']=total_score
        context['score']=self.request.session['score']
        return context

    





        
        