# Generated by Django 4.0.4 on 2022-05-31 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='secret_key',
            field=models.CharField(default='5LRI7OF5UFVVEGYHLGIF4NK752EYL4HZ', max_length=20),
        ),
    ]
