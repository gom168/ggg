# Generated by Django 3.2.7 on 2021-11-26 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_notesconfig_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notesconfig',
            name='comment_num',
        ),
        migrations.RemoveField(
            model_name='notesconfig',
            name='file',
        ),
        migrations.RemoveField(
            model_name='usercomment',
            name='add_time',
        ),
        migrations.RemoveField(
            model_name='usercomment',
            name='file',
        ),
    ]