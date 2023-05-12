# Generated by Django 4.1.7 on 2023-05-12 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=64, verbose_name='用户id')),
                ('channel_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='channel_name')),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avator_url', models.CharField(max_length=60, verbose_name='头像链接')),
                ('name', models.CharField(max_length=40, verbose_name='昵称')),
                ('phone', models.CharField(max_length=20, verbose_name='电话号码')),
                ('qq', models.CharField(max_length=30, verbose_name='qq号')),
                ('wechat', models.CharField(max_length=40, verbose_name='微信号')),
            ],
        ),
        migrations.CreateModel(
            name='LostAndFound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='物品名称')),
                ('time', models.DateTimeField(verbose_name='丢失时间')),
                ('place', models.CharField(max_length=60, verbose_name='丢失地点')),
                ('description', models.TextField(blank=True, null=True, verbose_name='文字介绍')),
                ('type', models.IntegerField(choices=[(1, '失物'), (2, '寻物')], verbose_name='类型')),
                ('state', models.BooleanField(default=1, verbose_name='状态')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=60, verbose_name='图片链接')),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='login.lostandfound', verbose_name='物品')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.CharField(max_length=200, unique=True, verbose_name='聊天室id')),
                ('content', models.TextField(verbose_name='聊天内容')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='login.information')),
            ],
        ),
    ]
