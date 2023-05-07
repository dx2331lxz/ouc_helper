from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from ouc_helper import settings
# 邮件
from utils.verification_code import make_code
from utils.verification_register import verification_password, verification_username
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from email.mime.text import MIMEText  #html格式和文本格式邮件

# jwt
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        re_password = data.get('re_password', '')
        code = data.get('code', '')
        if username == '' or password == '':
            return Response({'msg': '请输入用户名或密码', 'code': 403}, status=status.HTTP_403_FORBIDDEN)
        if re_password == '':
            return Response({'msg': '请输入确认密码', 'code': 403}, status=status.HTTP_403_FORBIDDEN)
        if verification_username(username) != 1:
            return Response(verification_username(username), status=status.HTTP_403_FORBIDDEN)
        if verification_password(password, re_password) != 1:
            return Response(verification_password(password, re_password), status=status.HTTP_403_FORBIDDEN)
        if code == '':
            return Response({'msg': '请输入邮件验证码', 'code': 403}, status=status.HTTP_403_FORBIDDEN)
        if code != request.session.get('code', ''):
            return Response({'msg': '验证码错误', 'code': 403}, status=status.HTTP_403_FORBIDDEN)
        User.objects.create_user(username=username, password=password)
        return Response({'msg': '注册成功', 'code': 200}, status=status.HTTP_200_OK)


class EmailVerificationAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        data = request.data
        email = data.get('email', '')
        if email == '':
            return Response({'msg': '请输入邮箱', 'code': 403}, status=status.HTTP_403_FORBIDDEN)
        code = str(make_code())
        subject = '海之子助手注册验证'
        text_content = '爱特工作室'
        html_content = """<div style="box-sizing: border-box;width: 98%;margin: 0 auto;max-width: 508px;background-color: #FFFFFF;border: 1px solid #f6f6f6;box-shadow: 0px 0 10px rgba(0, 0, 0, 0.08);border-radius: 8px;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" class="main-table_zZLU"
           style="width:100%;height:100%"></table>
    <table align="center" border="0" cellpadding="0" cellspacing="0"
           style="max-width: 508px; width: 100%; margin: 0 auto">
        <tbody>
        <tr>
            <td>
                <div style=" text-align: center; width: 100%; overflow: hidden; height: 100%; border-top-left-radius: 8px; border-top-right-radius: 8px; ">
                    <img style="width: 100%" src="https://image.daoxuan.cc/image/202305070019380.png"></div>
            </td>
        </tr>
        </tbody>
    </table>
    <table align="center" border="0" cellpadding="0" cellspacing="0" class="logo-table_NOgq"
           style=" max-width: 508px; width: 100%; background: #ffffff; margin: 15px auto 8px; ">
        <tbody>
        <tr>
            <td style="padding: 0 24px;"><p
                    style=" margin: 0 auto; font-family: HarmonyOS Sans, SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif; font-style: normal; font-weight: 900; font-size: 18px; line-height: 130%; color: #000000; width: 100%; overflow-wrap: break-word; word-break: break-word; text-align: left; ">
                验证邮箱</p></td>
        </tr>
        </tbody>
    </table>
    <table align="center" border="0" cellpadding="0" cellspacing="0" class="logo-table_NOgq"
           style=" max-width: 508px; width: 100%; margin: 0 auto; background: #ffffff">
        <tbody>
        <tr>
            <td style="text-align: center;padding: 0 24px"><p class="normal-font_oArV"
                                                              style=" margin: 0 auto; overflow-wrap: break-word; word-break: break-word; text-align: left; width: 100%; font-family: HarmonyOS Sans, SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 150%; color: #000000; ">
                <span class="bold-font_QRvu"
                      style=" font-style: inherit; font-family: inherit; font-size: inherit; line-height: inherit; text-indent: inherit; letter-spacing: inherit; color:inherit; font-weight: 600; ">您正在验证邮箱</span>，验证码：
            </p></td>
        </tr>
        </tbody>
    </table>
    <table align="center" border="0" cellpadding="0" cellspacing="0" class="logo-table_NOgq"
           style=" max-width: 508px; width: 100%; margin: 0 auto; background: #ffffff; margin-top: 12px">
        <tbody>
        <tr>
            <td style="padding: 0 24px;">
                <div class="code_GPAV"
                     style="letter-spacing:0.05em;font-size:28px;color:#000000;white-space:nowrap;font-style:normal;font-weight:500;text-align:left;font-family:HarmonyOS Sans, SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif;">
                    <span style="border-bottom:1px dashed #ccc;z-index:1" t="7" onclick="return false;"
                          data="">{}</span></div>
            </td>
        </tr>
        </tbody>
    </table>
    <table align="center" border="0" cellpadding="0" cellspacing="0" class="logo-table_NOgq"
           style=" max-width: 508px; width: 100%; margin: 0 auto; background: #ffffff">
        <tbody>
        <tr>
            <td style="text-align: center;padding: 0 24px"><p class="normal-font_oArV"
                                                              style=" margin: 0 auto; overflow-wrap: break-word; word-break: break-word; text-align: left; width: 100%; font-family: HarmonyOS Sans, SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 150%; color: #000000; ">
            </p></td>
        </tr>
        </tbody>
    </table>
    <table align="center" border="0" cellpadding="0" cellspacing="0" class="img_nOyV"
           style="max-width: 508px; width: 100%; margin-top:10px">
        <tbody>
        <tr class="title-logo_nESf">
            <td>
                <div class="new-line_YPVI" style="height:0px;display:block;width:100%"></div>
            </td>
        </tr>
        </tbody>
    </table>
    <table align="center" border="0" cellpadding="0" cellspacing="0" class="logo-table_NOgq"
           style=" max-width: 508px; width: 100%; margin: 0 auto; background: #ffffff">
        <tbody>
        <tr>
            <td style="text-align: center;padding: 0 24px"><p class="normal-font_oArV"
                                                              style=" margin: 0 auto; overflow-wrap: break-word; word-break: break-word; text-align: left; width: 100%; font-family: HarmonyOS Sans, SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 150%; color: #000000; ">

                验证码<span class="bold-font_QRvu"
                            style=" font-style: inherit; font-family: inherit; font-size: inherit; line-height: inherit; text-indent: inherit; letter-spacing: inherit; color:inherit; font-weight: 600; "> 1 分钟</span>内有效，请勿泄露。如非本人操作，请立即联系客服团队。

            </p></td>
        </tr>
        </tbody>
    </table>
    <table align="center" border="0" cellpadding="0" cellspacing="0"
           style=" background:rgba(255,255,255,1); max-width:508px; width:100%; margin:60px auto 0;">
        <tbody>
        <tr>
            <td style="padding: 0 24px;">
                <div style=" font-family: HarmonyOS Sans, SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif; text-align:left; font-size: 14px; font-weight: 400; line-height: 150%; color:#000000">
                    爱特工作室
                </div>
            </td>
        </tr>
        </tbody>
    </table>
    <p class="normal-font_oArV"
       style="margin:0 auto;overflow-wrap:break-word;word-break:break-word;text-align:left;width:90%;font-family:SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif;font-size:14px;line-height:20px;font-weight:normal;color:#000000"></p>
    <table align="center" border="0" cellpadding="0" cellspacing="0" class="logo-table_NOgq" style=" width: 100%;">
        <tbody>
        <tr>
            <td style="text-align: center">
                <div style=" box-sizing: border-box; max-width: 508px; margin: 0 auto; background: #f9f9f9; margin-top: 70px; padding: 15px 24px 28px; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; ">
                    <div style=" font-family: HarmonyOS Sans, SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif; font-weight: 400; font-size: 12px; line-height: 17px; text-align: center; color: #7D7D7D; ">
                        爱特工作室致力于保护您的账户和交易安全<br> - 如果您怀疑自己收到了诈骗信息，请立即联系客服 -
                        请勿与任何人分享您的验证码，包括官方客服和工作人员
                    </div>
                    <div style=" margin: 14px auto 12px; background-image: url('https://static.coinall.ltd/cdn/banner/20221205/16702339641035d61f6bf-822b-4c10-a25a-23fd6b74d4df.png'); background-size: 100% 10px; background-repeat: no-repeat; background-position: center;">
                        <span style="background-color: #f9f9f9;; padding: 0 15px;"><span style="height: 15px;"><img
                                src="https://static.coinall.ltd/cdn/oksupport/headImg/20221117/1668687253371.png"
                                style="width: 14px; height: 14px; vertical-align: middle;"></span><span
                                style=" vertical-align: middle; height: 15px; padding-left: 4px; font-size: 14px; font-family: SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif; font-weight: 500; font-size: 14px; color: #000000; opacity: 0.8;">期待与您保持联系</span></span><span></span>
                    </div>
                    <div style=" margin: 0 auto; overflow-wrap: break-word; word-break: break-word; text-align: center; font-size: 11px; font-family: HarmonyOS Sans, SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif; font-weight: 400; color: #7d7d7d; line-height: 17px; ">
                        感谢您选择爱特工作室<br> 如果有任何问题，疑虑或建议，请联系爱特工作室客服
                    </div>
                </div>
            </td>
        </tr>
        </tbody>
    </table>
</div>
""".format(int(code))
        from_email = settings.EMAIL_HOST_USER
        receive_email_addr = [email]
        msg = EmailMultiAlternatives(subject, text_content, from_email, receive_email_addr)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        request.session['code'] = code
        return Response({'msg': '发送成功', 'code': 200}, status=status.HTTP_200_OK)