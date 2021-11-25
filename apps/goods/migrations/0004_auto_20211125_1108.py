# Generated by Django 3.2.7 on 2021-11-25 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20211118_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='goods',
        ),
        migrations.AddField(
            model_name='settings',
            name='goods_sn',
            field=models.CharField(default=405, max_length=50, verbose_name='商品唯一货号'),
            preserve_default=False,
        ),
    ]