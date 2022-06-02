import datetime
from numpy import ones_like

from pyotp import TOTP
from .models import TimeStarted, Topic, Question, Answer, UserRecord
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView,View
from users.models import CustomUser



@method_decorator(login_required, name='dispatch')
class TopicView(ListView):
    model = Topic
    template_name = 'quiz/topic.html'
    context_object_name = 'topics'


class QuestionView(View):
    template_name="quiz/quizz.html"

    def get_context_data(self, **kwargs):
        user_object=CustomUser.objects.get(username=self.request.user)
        if user_object.email_confirmed:
            context={}
            t_id=self.kwargs.get('t_id')
            topic = Topic.objects.get(id=t_id)
            time_object=TimeStarted.objects.get_or_create(user=self.request.user, topic=topic)
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
                total_questions.append(str(question.id))
            user_answered=UserRecord.objects.filter(user=self.request.user).filter(topic=t_id)
            answered_list=[]
            for answered_question in user_answered:
                answered_list.append(str(answered_question.question.id))   
            for question_id in total_questions:
                if question_id not in answered_list:
                    questionset=Question.objects.filter(id=question_id)
                    for question in questionset:
                        if question.type=="mcq":
                            answerset=Answer.objects.filter(question=question_id)
                            out_of=len(total_questions)
                            current=len(answered_list)+1
                            context['questionset']=questionset
                            context['answerset']=answerset
                            context['out_of']=out_of
                            context['current']=current
                            context['time_left']=time_left
                            return context
                        else:
                            print(question.type, question.id,question.text)
                            out_of=len(total_questions)
                            current=len(answered_list)+1
                            context['questionset']=questionset
                            context['out_of']=out_of
                            context['current']=current
                            context['time_left']=time_left
                            return context
        else:
            return HttpResponseRedirect(reverse('validate', kwargs={'user':self.request.user}))
        
        

    def post(self, request, *args, **kwargs):
        user_object=CustomUser.objects.get(username=self.request.user)
        if user_object.email_confirmed:
            t_id=self.kwargs.get('t_id')
            question_id=self.request.POST.get('hidden1')
            question_object=Question.objects.get(id=question_id)
            topic_object=Topic.objects.get(id=t_id)
            if question_object.type=="mcq":
                answer_id=self.request.POST.get(question_object.text)
                answer_object=Answer.objects.get(id=answer_id)
                query=UserRecord(user=self.request.user,question=question_object,answer_choosen=answer_object,topic=topic_object)
                query.save()
            else:
                oneline_answer=self.request.POST.get('oneline')                
                query=UserRecord(user=self.request.user, question=question_object,text_answer=oneline_answer,topic=topic_object)
                query.save()
            questions=Question.objects.filter(topic=t_id)
            total_questions=[]
            for question in questions:
                total_questions.append(str(question.id))
            user_answered=UserRecord.objects.filter(user=self.request.user).filter(topic=t_id)
            answered_list=[]
            for answered_question in user_answered:
                answered_list.append(str(answered_question.question.id))
            if len(user_answered)<len(total_questions):
                return HttpResponseRedirect(reverse('quiz',kwargs={'t_id':t_id}))
            else:
                return HttpResponseRedirect(reverse('score', kwargs={"t_id":t_id}))
        else:
            return HttpResponseRedirect(reverse('validate', kwargs={'user':self.request.user}))
        
    
    def get(self, request, *args, **kwargs):
        user_object=CustomUser.objects.get(username=self.request.user)
        if user_object.email_confirmed:
            t_id=self.kwargs.get('t_id')
            questions=Question.objects.filter(topic=t_id)
            total_questions=[]
            for question in questions:
                total_questions.append(str(question.id))
            user_answered=UserRecord.objects.filter(user=self.request.user).filter(topic=t_id)
            answered_list=[]
            for answered_question in user_answered:
                answered_list.append(str(answered_question.question.id))
            if len(user_answered)<len(total_questions):
                return render(request,self.template_name,self.get_context_data())
            else:
                return HttpResponseRedirect(reverse('score', kwargs={"t_id":t_id}))
        else:
            return HttpResponseRedirect(reverse('validate', kwargs={'user':self.request.user}))
        


class ScoreListView(ListView):
    model=UserRecord
    template_name="quiz/quizend.html"
    context_object_name="scores"

    def get_queryset(self):
        topic_id=self.kwargs.get('t_id')
        user_record=UserRecord.objects.filter(user=self.request.user).filter(topic=topic_id)
        return user_record
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_id=self.kwargs.get('t_id')
        user_record=UserRecord.objects.filter(user=self.request.user).filter(topic=topic_id)
        oneline_answer=[]
        total_score=0
        for score in user_record:
            if score.question.type=="mcq":
                if score.answer_choosen.is_correct:
                    total_score= total_score+1
            else:
                user_answer=score.text_answer
                question_id=score.question.id
                answer_object=Answer.objects.get(question=question_id)
                answer=answer_object.text
                oneline_answer.append({score.question:answer})
                if user_answer==answer:
                    total_score=total_score+1
        context['score']=total_score
        context['oneline_answer']=oneline_answer
        return context

    





        
        