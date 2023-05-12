from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Information(models.Model):
    user = models.ForeignKey(verbose_name='关联用户', to=User, to_field='id', on_delete=models.CASCADE)
    avator_url = models.CharField(verbose_name='头像链接', max_length=60)
    name = models.CharField(verbose_name='昵称', max_length=40)
    phone = models.CharField(verbose_name='电话号码', max_length=20)
    qq = models.CharField(verbose_name='qq号', max_length=30)
    wechat = models.CharField(verbose_name='微信号', max_length=40)


type_choices = (
    (1, '失物'),
    (2, '寻物')
)


class LostAndFound(models.Model):
    name = models.CharField(verbose_name='物品名称', max_length=40)
    time = models.DateTimeField(verbose_name='丢失时间')
    place = models.CharField(verbose_name='丢失地点', max_length=60)
    user = models.ForeignKey(verbose_name='关联用户', to=User, to_field='id', on_delete=models.CASCADE)
    description = models.TextField(verbose_name='文字介绍', blank=True, null=True)
    type = models.IntegerField(verbose_name='类型', choices=type_choices)
    state = models.BooleanField(verbose_name='状态', default=1)  # 1未找到，0已找到


class Picture(models.Model):
    url = models.CharField(verbose_name='图片链接', max_length=60)
    thing = models.ForeignKey(to_field='id', to='LostAndFound', on_delete=models.DO_NOTHING, verbose_name='物品')


class Message(models.Model):
    room_id = models.CharField(verbose_name='聊天室id', max_length=200)
    from_user = models.CharField(verbose_name='发消息的人', max_length=200)
    to_user = models.CharField(verbose_name='接收消息的人', max_length=200)
    content = models.TextField(verbose_name='聊天内容')


class Channel(models.Model):
    user_id = models.CharField(verbose_name='用户id', max_length=64)
    channel_name = models.CharField(verbose_name='channel_name', max_length=200, null=True, blank=True)
    group_id = models.CharField(verbose_name='组', max_length=64, default="0")
    status = models.BooleanField(verbose_name="是否在线", default=False)
