from quiz.models import Answer, Question, Topic, UserRecord
from rest_framework import serializers
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        user.send_otp()
        return user
    

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id','text', 'topic', 'type', 'answers']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['time'] = self.context['time']
        representation['current_question'] = self.context['current_question']
        representation['total_questions'] = self.context['total_questions']
        return representation


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRecord
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['score'] = self.context['score']
        return representation