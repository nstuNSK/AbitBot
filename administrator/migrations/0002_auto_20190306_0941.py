# Generated by Django 2.1.7 on 2019-03-06 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direction',
            name='description',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='direction',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
