from django.db import models
import uuid

DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)
    
class Subject(models.Model):

    s_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)

    subject_name = models.CharField(max_length=100)
    def __str__(self):
        return self.subject_name


class Topic(models.Model):
    t_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    topic = models.CharField(max_length=200)
    number_of_questions = models.IntegerField()
    time_required = models.IntegerField(help_text="Duration of Quizz in minutes")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score_to_pass = models.IntegerField(help_text="Minimum score to Pass in %", null=True)

    def __str__(self):
        return f"{self.topic} | {self.subject}"


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
    correct=models.BooleanField(default=False)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.answer} {self.correct}"

