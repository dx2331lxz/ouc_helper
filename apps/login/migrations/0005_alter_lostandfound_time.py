# Generated by Django 4.1.7 on 2023-05-17 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_remove_message_user_information_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lostandfound',
            name='time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='丢失时间'),
        ),
    ]
