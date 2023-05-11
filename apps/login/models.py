from django.db import models


# Create your models here.

class Information(models.Model):
    avator_url = models.CharField(verbose_name='头像链接', max_length=60)
    name = models.CharField(verbose_name='昵称', max_length=40)
    phone = models.CharField(verbose_name='电话号码', max_length=20)
    qq = models.CharField(verbose_name='qq号', max_length=30)
    wechat = models.CharField(verbose_name='微信号', max_length=40)


class Message(models.Model):
    room_id = models.CharField(verbose_name='聊天室id', max_length=200, unique=True)
    user = models.ForeignKey(to_field='id', to=Information, on_delete=models.DO_NOTHING)
    content = models.TextField(verbose_name='聊天内容')


class Channel(models.Model):
    user_id = models.CharField(verbose_name='用户id', max_length=64)
    channel_name = models.CharField(verbose_name='channel_name', max_length=200, null=True, blank=True)
