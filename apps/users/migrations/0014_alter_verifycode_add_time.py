# Generated by Django 3.2.7 on 2021-12-01 11:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_verifycode_add_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifycode',
            name='add_time',
            field=models.DateField(default=datetime.datetime(2021, 12, 1, 19, 38, 57, 580692), verbose_name='添加时间'),
        ),
    ]