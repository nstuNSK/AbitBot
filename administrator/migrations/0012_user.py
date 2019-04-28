# Generated by Django 2.1.7 on 2019-04-28 15:42

from django.db import migrations, models
from administrator.models import UserManager
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('administrator', '0011_auto_20190418_2057'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="User",
                    fields=[
                        (
                            "id",
                            models.AutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        )
                    ],
                    options={"db_table": "auth_user"},
                    managers=[("objects", UserManager())],
                )
            ]
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('firstName', models.CharField(max_length=50, verbose_name='Имя')),
                ('lastName', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('login', models.CharField(max_length=50, unique=True, verbose_name='Логин')),
                ('password', models.TextField(verbose_name='Пароль')),
                ('is_active', models.BooleanField(default=True, verbose_name='Аккаунт действует')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Сотрудник')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Администратор',
                'verbose_name_plural': 'Администраторы',
            },
        ),
    ]
