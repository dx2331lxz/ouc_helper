from django.contrib import admin
from apps.login.models import *

# Register your models here.
admin.site.site_header = '爱特管理后台'  # 设置header
admin.site.site_title = '失物招领管理后台'  # 设置title
admin.site.index_title = '失物招领管理后台'


class InformationAdmin(admin.ModelAdmin):
    # 新增和修改页面需要展示的字段
    fields = ('user', 'avatar_url', 'name', 'phone', 'qq', 'wechat')

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ['user', 'avatar_url', 'name', 'phone', 'qq', 'wechat', 'image_data']

    # 搜索
    search_fields = ['name', 'phone', 'qq', 'wechat']

    # 只读字段
    # readonly_fields = ('code', 'create_time', 'update_time')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

    # ordering设置默认排序字段，负号表示降序排序
    # ordering = ('-create_time',)

    # 设置哪些字段可以点击进入编辑界面
    # list_display_links = ('name',)
    # 详细时间分层筛选　
    # date_hierarchy = 'create_time'

    # list_editable 设置默认可编辑字段，这个字段必须要在list_display里面配置才可以使用
    # 并且必须表里面有对应字段，不能是自己定义的列表字段
    # list_editable = ['']

    # fk_fields 设置显示外键字段,如果这个表里面有外键，并且想要在列表展示，就可以使用这个配置
    fk_fields = ('user',)


class LostAndFoundAdmin(admin.ModelAdmin):
    fields = ('user','name', 'time', 'place','description', 'type', 'state', 'publish_time')

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ['user','name', 'time', 'place','description', 'type', 'state', 'publish_time']

    # 搜索
    search_fields = ['name', 'time', 'place', 'type', 'state', 'publish_time']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

    # fk_fields 设置显示外键字段,如果这个表里面有外键，并且想要在列表展示，就可以使用这个配置
    fk_fields = ('user',)


class PictureAdmin(admin.ModelAdmin):
    fields = ('thing', 'url')

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ['thing', 'url']

    # 搜索
    # search_fields = ['name', 'time', 'place', 'type', 'state', 'publish_time']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

    # fk_fields 设置显示外键字段,如果这个表里面有外键，并且想要在列表展示，就可以使用这个配置
    fk_fields = ('thing',)


class MessageAdmin(admin.ModelAdmin):
    fields = ('room_id', 'from_user', 'to_user', 'content')

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ['room_id', 'from_user', 'to_user', 'content']

    # 搜索
    search_fields = ['room_id', 'from_user', 'to_user']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

    # fk_fields 设置显示外键字段,如果这个表里面有外键，并且想要在列表展示，就可以使用这个配置
    # fk_fields = ('user',)
class ChannelAdmin(admin.ModelAdmin):
    fields = ('user', 'channel_name', 'group_id', 'status')

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ['user', 'channel_name', 'group_id', 'status']

    # 搜索
    search_fields = ['status',]

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5

    fk_fields = ('user',)

admin.site.register(Information, InformationAdmin)
admin.site.register(LostAndFound, LostAndFoundAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Group)
