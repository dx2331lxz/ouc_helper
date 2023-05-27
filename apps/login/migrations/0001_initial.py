# Generated by Django 4.1.4 on 2023-05-24 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.CharField(default='0', max_length=64, verbose_name='组')),
                ('widget_user_ids', django_mysql.models.ListTextField(models.IntegerField(), size=10)),
            ],
            options={
                'verbose_name': '聊天室',
                'verbose_name_plural': '聊天室',
            },
        ),
        migrations.CreateModel(
            name='LostAndFound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='物品名称')),
                ('time', models.DateTimeField(blank=True, null=True, verbose_name='丢失时间')),
                ('place', models.CharField(max_length=60, verbose_name='丢失地点')),
                ('description', models.TextField(blank=True, null=True, verbose_name='文字介绍')),
                ('type', models.IntegerField(choices=[(1, '失物'), (2, '寻物')], verbose_name='类型')),
                ('state', models.BooleanField(default=1, verbose_name='状态')),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '物品信息',
                'verbose_name_plural': '物品信息',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.CharField(max_length=200, verbose_name='聊天室id')),
                ('from_user', models.CharField(max_length=200, verbose_name='发消息的人')),
                ('to_user', models.CharField(max_length=200, verbose_name='接收消息的人')),
                ('content', models.TextField(verbose_name='聊天内容')),
            ],
            options={
                'verbose_name': '聊天离线记录',
                'verbose_name_plural': '聊天离线记录',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200, verbose_name='图片链接')),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='login.lostandfound', verbose_name='物品')),
            ],
            options={
                'verbose_name': '图片信息',
                'verbose_name_plural': '图片信息',
            },
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar_url', models.CharField(default='https://picture.daoxuan.cc/image/202301301254377.webp', max_length=200, verbose_name='头像链接')),
                ('name', models.CharField(default='昵称', max_length=40, verbose_name='昵称')),
                ('phone', models.CharField(default='', max_length=20, verbose_name='电话号码')),
                ('qq', models.CharField(default='', max_length=30, verbose_name='qq号')),
                ('wechat', models.CharField(default='', max_length=40, verbose_name='微信号')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '个人信息',
                'verbose_name_plural': '个人信息',
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='channel_name')),
                ('group_id', django_mysql.models.ListTextField(models.IntegerField(), size=10)),
                ('status', models.BooleanField(default=False, verbose_name='是否在线')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '个人频道',
                'verbose_name_plural': '个人频道',
            },
        ),
    ]
