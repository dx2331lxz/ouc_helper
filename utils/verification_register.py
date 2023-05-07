from django.contrib.auth.models import User


def verification_username(username):
    for i in username:
        if u"\u4e00" < i < u"\u9fff" or not username.isalnum():
            error = "用户名只能包含字母和数字"
            return {'msg': error, 'code': 403}
        try:
            User.objects.get(username=username)
            error = '该用户名已存在'
            return {'msg': error, 'code': 403}
        except User.DoesNotExist:
            pass
    return 1


def verification_password(password, re_password):
    if re_password != password:
        error = "两次输入密码不一样"
        return {'msg': error, 'code': 403}
    return 1
