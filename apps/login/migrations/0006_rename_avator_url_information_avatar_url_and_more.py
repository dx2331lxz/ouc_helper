# Generated by Django 4.1.7 on 2023-05-18 02:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_alter_lostandfound_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='information',
            old_name='avator_url',
            new_name='avatar_url',
        ),
        migrations.AddField(
            model_name='lostandfound',
            name='publish_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间'),
        ),
    ]