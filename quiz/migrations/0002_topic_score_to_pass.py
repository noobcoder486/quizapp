# Generated by Django 4.0.3 on 2022-04-30 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='score_to_pass',
            field=models.IntegerField(help_text='Minimum score to Pass in %', null=True),
        ),
    ]