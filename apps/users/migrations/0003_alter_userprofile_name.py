# Generated by Django 3.2.7 on 2021-11-18 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userprofile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='姓名'),
        ),
    ]