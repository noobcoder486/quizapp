# Generated by Django 4.0.4 on 2022-05-26 11:59

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0015_remove_userrecord_time_interval'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Time_Started',
            new_name='TimeStarted',
        ),
        migrations.AlterModelOptions(
            name='timestarted',
            options={'verbose_name_plural': 'TimeStarted'},
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='a_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='answer',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='q_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='question',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='t_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='topic',
            new_name='name',
        ),
    ]
