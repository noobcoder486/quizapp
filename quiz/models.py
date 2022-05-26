import uuid
from django.contrib.auth.models import User
from django.db import models



class Topic(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    name = models.CharField(max_length=200)
    time_required = models.IntegerField(help_text="Duration of Quizz in seconds")

    def __str__(self):
        return f"{self.name}"


class Question(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    text = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Answer(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    text= models.CharField(max_length=100)
    is_correct=models.BooleanField(default=False)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.text}"


class UserRecord(models.Model):
    User=models.ForeignKey(User, on_delete=models.CASCADE)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_choosen=models.ForeignKey(Answer, on_delete=models.CASCADE)
    topic=models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.User} | {self.question} | {self.answer_choosen} | {self.answer_choosen.is_correct}"


class TimeStarted(models.Model):
    User=models.ForeignKey(User, on_delete=models.CASCADE)
    topic=models.ForeignKey(Topic, on_delete=models.CASCADE)
    starting_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.User} | {self.starting_time.time()}"

    class Meta:
        verbose_name_plural='TimeStarted'
