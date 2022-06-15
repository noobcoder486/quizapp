import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from django.urls import reverse
from django.views.generic import ListView,View

from users.mixins import UserVerifiedMixin

from . models import Topic, Question, Answer, UserRecord, TimeStarted



class TopicView(UserVerifiedMixin, ListView):
    model = Topic
    template_name = 'quiz/topic.html'
    context_object_name = 'topics'


class QuestionView(UserVerifiedMixin, View):
    template_name="quiz/quizz.html"

    def get_context_data(self, **kwargs):
        context={}
        topic_id = self.kwargs.get('topic_id')
        topic = Topic.objects.get(id = topic_id)
        time_object = TimeStarted.objects.get_or_create(user = self.request.user, topic=topic)
        starting_time_object = time_object[0]
        quiz_start_time = starting_time_object.starting_time #starting time
        current_time = datetime.datetime.now()
        difference = current_time - quiz_start_time
        difference_in_seconds = difference.seconds
        total_time_in_seconds = topic.time_required
        if total_time_in_seconds > difference_in_seconds:
            time_left=int(total_time_in_seconds - difference_in_seconds)
        else:
            time_left = -1

        #getting the question refering topic id
        question_ids=Question.objects.filter(topic=topic_id).values_list('id', flat=True)
        # total_questions=[]
        # for question in questions:
        #     total_questions.append(str(question.id))

        user_answered=UserRecord.objects.filter(user=self.request.user, topic=topic_id)
        answered_list=[]
        for answered_question in user_answered:
            answered_list.append(str(answered_question.question.id))

        for question_id in question_ids:
            if str(question_id) not in answered_list:
                question=Question.objects.get(id=question_id)
                # for question in questionset:
                if question.type==Question.MCQ:
                    answerset=Answer.objects.filter(question = question_id)
                    context['answerset']=answerset
                context['out_of']=len(question_ids)
                context['current']=len(answered_list)+1
                context['question']=question
                context['time_left']=time_left
                return context
        
    def post(self, request, *args, **kwargs):
        topic_id = self.kwargs.get('topic_id')
        question_id = self.request.POST.get('hidden1')
        question_object = Question.objects.get(id = question_id)
        topic_object = Topic.objects.get(id = topic_id)
        if question_object.type == Question.MCQ:
            answer_id = self.request.POST.get(question_object.text)
            answer_object = Answer.objects.get(id=answer_id)
            if UserRecord.objects.filter(user=self.request.user, question= question_object).exists():
                messages.info(f"The particular has been already recorded.")
            else:
                query = UserRecord(user = self.request.user,question = question_object,answer_choosen = answer_object,topic = topic_object)
                query.save()
        else:
            oneline_answer = self.request.POST.get('oneline')
            if UserRecord.objects.filter(user=self.request.user, question= question_object).exists():
                messages.info(f"The particular has been already recorded.")
            else:
                query = UserRecord(user=self.request.user, question=question_object, text_answer=oneline_answer, topic=topic_object)
                query.save()
        questions = Question.objects.filter(topic=topic_id)
        total_questions=[]
        for question in questions:
            total_questions.append(str(question.id))
        user_answered = UserRecord.objects.filter(user=self.request.user).filter(topic=topic_id)
        answered_list = []
        for answered_question in user_answered:
            answered_list.append(str(answered_question.question.id))
        if len(user_answered) < len(total_questions):
            return HttpResponseRedirect(reverse('quiz',kwargs={'topic_id':topic_id}))
        else:
            return HttpResponseRedirect(reverse('score', kwargs={"topic_id":topic_id}))

    
    def get(self, request, *args, **kwargs):
        topic_id = self.kwargs.get('topic_id')
        question_ids = Question.objects.filter(topic=topic_id).values_list("id", flat = True)

        user_answered = UserRecord.objects.filter(user=self.request.user, topic= topic_id)
        answered_list = []
        for answered_question in user_answered:
            answered_list.append(str(answered_question.question.id))

        if len(user_answered) < len(question_ids):
            return render(request,self.template_name,self.get_context_data())
        else:
            return HttpResponseRedirect(reverse('score', kwargs={"topic_id":topic_id}))
        


class ScoreListView(ListView):
    model = Question
    template_name = "quiz/quizend.html"
    context_object_name = "questions"

    def get_queryset(self):
        topic_id = self.kwargs.get('topic_id')
        questions = Question.objects.filter(topic=topic_id)
        return questions
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_id=self.kwargs.get('topic_id')
        questions = context['questions']
        user_record_context = []
        user_records = UserRecord.objects.filter(user=self.request.user, topic=topic_id)
        for question in questions:
            for record in user_records:
                if question.id == record.question.id:
                    if record.question.type == Question.MCQ:
                        answer = record.answer_choosen
                    else:
                        answer = record.text_answer
                    # answer = record.answer_chosen or record.text_answer
                    user_record_context.append({question:answer})
        total_score = 0
        for score in user_records:
            if score.question.type == Question.MCQ:
                if score.answer_choosen.is_correct:
                    total_score = total_score+1
            else:
                user_answer = score.text_answer
                question_id = score.question.id
                answer_object = Answer.objects.get(question=question_id)
                answer = answer_object.text
                if user_answer == answer:
                    total_score = total_score + 1
        context['user'] = self.request.user
        context['score'] = total_score
        context['results'] = user_record_context
        return context

    





        
        