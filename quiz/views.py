from graphlib import TopologicalSorter
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Topic, Question, Answer, UserRecord
from django.utils.decorators import method_decorator
from django.shortcuts import render,redirect
from django.urls import reverse


@method_decorator(login_required, name='dispatch')
class TopicView(ListView):
    model = Topic
    template_name = 'quiz/topic.html'
    context_object_name = 'topics'

    

def nextques(request,t_id):
    if request.method=="POST":
        user=request.user
        question_id=request.POST.get('hidden1')     
        question=request.POST.get('hidden')
        answer_id=request.POST.get(question)
        topic_object=Topic.objects.get(t_id=t_id)
        print(topic_object)
        query=UserRecord(User=user,question=question_id,answer_choosen=answer_id,topic=topic_object)
        query.save()
    questions=Question.objects.filter(topic=t_id)
    total_questions=[]
    for question in questions:
        total_questions.append(str(question.q_id))
    user_answered=UserRecord.objects.filter(User=request.user).filter(topic=t_id)
    answered_list=[]
    for answered_question in user_answered:
        answered_list.append(str(answered_question.question))
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
        return render(request, "quiz/quizend.html")


    





        
        