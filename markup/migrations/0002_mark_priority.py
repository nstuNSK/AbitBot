# Generated by Django 2.1.7 on 2020-03-16 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='priority',
            field=models.IntegerField(default=1, verbose_name='Приоритет'),
        ),
    ]