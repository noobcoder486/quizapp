# Generated by Django 4.0.4 on 2022-05-24 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_time_started'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time_started',
            name='starting_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]