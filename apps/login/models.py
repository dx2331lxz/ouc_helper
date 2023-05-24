from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import format_html
from django_mysql.models import ListTextField
from django.utils.safestring import mark_safe
# Create your models here.


class Information(models.Model):
    user = models.ForeignKey(verbose_name='关联用户', to=User, to_field='id', on_delete=models.CASCADE)
    avatar_url = models.CharField(verbose_name='头像链接', max_length=200,
                                  default='https://picture.daoxuan.cc/image/202301301254377.webp')
    name = models.CharField(verbose_name='昵称', max_length=40, default='昵称')
    phone = models.CharField(verbose_name='电话号码', max_length=20, default='')
    qq = models.CharField(verbose_name='qq号', max_length=30, default='')
    wechat = models.CharField(verbose_name='微信号', max_length=40, default='')

    class Meta:
        verbose_name = "个人信息"
        verbose_name_plural = "个人信息"

    def __str__(self):
        return self.name

    def image_data(self):
        if self.avatar_url:
            html_img = """  
                <div onclick='$(".my_set_image_img").hide();$(this).next().show();'>
                <img src='{}' style='width:50px;height:50px;' title='点击可看大图'>
                <br/>
                </div>


                <div class='my_set_image_img' onclick="$('.my_set_image_img').hide()" style="z-index:9999;position:fixed; left: 100px; top:100px;display:none;">
                <img src='{}' style='width: 502px;height:500px;margin-left: 200px;' title='点击关闭'>
                </div>




                """.format(self.avatar_url, self.avatar_url)
            return mark_safe(html_img)
        else:
            return format_html(
                '<span>无照片</span>',
            )

    image_data.short_description = '头像缩略图'


type_choices = (
    (1, '失物'),
    (2, '寻物')
)


class LostAndFound(models.Model):
    user = models.ForeignKey(verbose_name='关联用户', to=User, to_field='id', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='物品名称', max_length=40)
    time = models.DateTimeField(verbose_name='丢失时间', blank=True, null=True)
    place = models.CharField(verbose_name='丢失地点', max_length=60)
    description = models.TextField(verbose_name='文字介绍', blank=True, null=True)
    type = models.IntegerField(verbose_name='类型', choices=type_choices)
    state = models.BooleanField(verbose_name='状态', default=1)  # 1未找到，0已找到
    publish_time = models.DateTimeField(verbose_name='发布时间', default=timezone.now)

    class Meta:
        verbose_name = "物品信息"
        verbose_name_plural = "物品信息"

    def __str__(self):
        return self.name

class Picture(models.Model):
    url = models.CharField(verbose_name='图片链接', max_length=200)
    thing = models.ForeignKey(to_field='id', to='LostAndFound', on_delete=models.DO_NOTHING, verbose_name='物品')

    class Meta:
        verbose_name = "图片信息"
        verbose_name_plural = "图片信息"

class Message(models.Model):
    room_id = models.CharField(verbose_name='聊天室id', max_length=200)
    from_user = models.CharField(verbose_name='发消息的人', max_length=200)
    to_user = models.CharField(verbose_name='接收消息的人', max_length=200)
    content = models.TextField(verbose_name='聊天内容')

    class Meta:
        verbose_name = "聊天离线记录"
        verbose_name_plural = "聊天离线记录"

class Channel(models.Model):
    # user_id = models.CharField(verbose_name='用户id', max_length=64)
    user = models.ForeignKey(verbose_name='关联用户', to=User, to_field='id', on_delete=models.CASCADE)
    channel_name = models.CharField(verbose_name='channel_name', max_length=200, null=True, blank=True)
    group_id = ListTextField(
        base_field=models.IntegerField(),
        size=10,  # Maximum of 100 ids in list
    )
    status = models.BooleanField(verbose_name="是否在线", default=False)

    class Meta:
        verbose_name = "个人频道"
        verbose_name_plural = "个人频道"
class Group(models.Model):
    group_id = models.CharField(verbose_name='组', max_length=64, default="0")
    widget_user_ids = ListTextField(
        base_field=models.IntegerField(),
        size=10,  # Maximum of 100 ids in list
    )

    class Meta:
        verbose_name = "聊天室"
        verbose_name_plural = "聊天室"

