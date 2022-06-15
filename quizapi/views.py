import datetime
from quiz.models import Answer, Question, TimeStarted, Topic, UserRecord
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser
from .serializers import QuestionSerializer, TopicSerializer, UserSerializer,ScoreSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ValidateAPIView(APIView):

    def post(self, request):
        otp = request.data.get("otp")
        user = self.request.user
        if user.email_confirmed:
            return Response(data = {"Response": f"User is already validated!"})
        else:
            verify_otp = user.verify_otp(otp)
            if verify_otp:
                return Response(data = {"Response": f"OTP validation successfull for {user}"})
            else:
                return Response(data = {"Response": f"OTP is Incorrect"})
        

class ResendOtpAPIView(APIView):
    
    def get(self, request):
        user= self.request.user
        user.send_otp()
        return Response(data={"Response":f"OTP sent successfully on {user.email}"})


class TopicAPIView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (AllowAny,)


class QuestionAPIView(APIView):
    serializer_class = QuestionSerializer

    def get(self, request, **kwargs):
        topic_id = self.kwargs.get("topic_id")
        topic = Topic.objects.get(id=topic_id)
        time_object = TimeStarted.objects.get_or_create(user=self.request.user, topic=topic)
        starting_time_object = time_object[0]
        quiz_start_time = starting_time_object.starting_time  # starting time
        current_time = datetime.datetime.now()
        difference = current_time - quiz_start_time
        difference_in_seconds = difference.seconds
        total_time_in_seconds = topic.time_required
        if total_time_in_seconds > difference_in_seconds:
            time_left = int(total_time_in_seconds - difference_in_seconds)
        else:
            time_left = -1

        question_ids = Question.objects.filter(
            topic=topic_id).values_list("id", flat=True)
        user_answered = UserRecord.objects.filter(
            user=self.request.user, topic=topic_id)
        answered_list = []
        for answered_question in user_answered:
            answered_list.append(str(answered_question.question.id))

        if len(answered_list) == len(question_ids):
            return Response(data={"Response": "All the questions has been successfully attempted"})
        else:
            for question_id in question_ids:
                if str(question_id) not in answered_list:
                    question = Question.objects.get(id=question_id)
            serializer = QuestionSerializer(question, context={'time': time_left,
                                                               'current_question': len(answered_list)+1,
                                                               'total_questions': len(question_ids),
                                                               }
                                            )
            return Response(serializer.data)

    def post(self, request, **kwargs):
        topic_id = self.kwargs.get('topic_id')
        topic_object = Topic.objects.get(id=topic_id)
        question_id = request.data.get("question_id")
        question_object = Question.objects.get(id=question_id)
        answer_id = request.data.get("answer_id")
        if question_object.type == Question.MCQ:
            answer_id = request.data.get("answer_id")
            answer_object = Answer.objects.get(id=answer_id)
            if UserRecord.objects.filter(user=self.request.user, question=question_id).exists():
                return Response(data={"Response": "The question has been previously attempted by the user"})
            else:
                query = UserRecord(user=self.request.user, question=question_object,
                                   answer_choosen=answer_object, topic=topic_object)
                query.save()
        else:
            oneline_answer = request.data.get("oneline")
            if UserRecord.objects.filter(user=self.request.user, question=question_id).exists():
                return Response(data={"Response": "The question has been previously attempted by the user"})
            else:
                query = UserRecord(user=self.request.user, question=question_object,
                                   text_answer=oneline_answer, topic=topic_object)
                query.save()
        return Response("Record Posted Successfully")


class ScoreAPIView(generics.ListAPIView):
    serializer_class = ScoreSerializer

    def get(self, request, **kwargs):
        topic_id = self.kwargs.get("topic_id")
        topic_object = Topic.objects.get(id = topic_id)
        result = UserRecord.objects.filter(topic = topic_object, user = self.request.user)
        total_score = 0
        for score in result:
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
        serializer = ScoreSerializer(result, context={"score":total_score})
        return Response(serializer.data)
