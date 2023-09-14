# Generated by Django 4.2.4 on 2023-09-14 03:21

import apps.users.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_case_insensitive_collection'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', apps.users.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(db_collation='case_insensitive', max_length=254, unique=True, verbose_name='email'),
        ),
    ]
