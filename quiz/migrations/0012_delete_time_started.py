# Generated by Django 4.0.4 on 2022-05-24 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_alter_time_started_starting_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Time_Started',
        ),
    ]