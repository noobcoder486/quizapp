import uuid
from django.contrib.auth import get_user_model
from django.db import models


class Topic(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    name = models.CharField(max_length=200)
    time_required = models.IntegerField(help_text="Duration of Quiz in seconds")

    def __str__(self):
        return f"{self.name}"


class Question(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    text = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    MCQ = 'mcq'
    ONELINE = 'oneline'
    
    TYPES=(
        (MCQ, MCQ),
        (ONELINE, ONELINE),
    )
    type=models.CharField(max_length=10, choices=TYPES)

    def __str__(self):
        return f'{self.text}'

class Answer(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    text= models.CharField(max_length=100)
    is_correct=models.BooleanField(default=False)
    question=models.ForeignKey(Question, on_delete=models.CASCADE,related_name="answerset")
    

    def __str__(self):
        return f"{self.text}"


class UserRecord(models.Model):
    user=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_choosen=models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    text_answer=models.CharField(max_length=100)
    topic=models.ForeignKey(Topic, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user} | {self.question} | {self.answer_choosen} | {self.text_answer}"

    class Meta:
        verbose_name_plural='User Records'

class TimeStarted(models.Model):
    user=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    topic=models.ForeignKey(Topic, on_delete=models.CASCADE)
    starting_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user} | Time: {self.starting_time.time()} | Topic: {self.topic}"

    class Meta:
        verbose_name_plural='Times Started'
