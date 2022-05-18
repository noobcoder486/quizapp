from django.db import models
from django.contrib.auth.models import User
import uuid

class Topic(models.Model):
    t_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    topic = models.CharField(max_length=200)
    time_required = models.IntegerField(help_text="Duration of Quizz in minutes")

    def __str__(self):
        return f"{self.topic}"


class Question(models.Model):
    q_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    question = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class Answer(models.Model):
    a_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    answer= models.CharField(max_length=100)
    is_correct=models.BooleanField(default=False)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.answer}"


class UserRecord(models.Model):
    User=models.ForeignKey(User, on_delete=models.CASCADE)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_choosen=models.ForeignKey(Answer, on_delete=models.CASCADE)
    topic=models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.User} | {self.question} | {self.answer_choosen} | {self.answer_choosen.is_correct}"

