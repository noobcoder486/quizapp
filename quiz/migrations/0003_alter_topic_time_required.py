# Generated by Django 4.0.4 on 2022-05-20 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_alter_userrecord_answer_choosen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='time_required',
            field=models.IntegerField(help_text='Duration of Quizz in seconds'),
        ),
    ]