from django.shortcuts import render, HttpResponse, redirect
from .forms import loginForm
from django.contrib.auth import authenticate, login
# from .api import check_cookie, check_login, get_all_major, DecimalEncoder, get_all_class, get_all_type, is_login
# from .models import MajorInfo, UserType, UserInfo, ClassInfo, Attendence, Notice, Leave, ExamContent, Exam
from .api import check_cookie, check_login, DecimalEncoder, is_login, check_teacher_login, teacher_check_cookie, \
    is_teacher_login, check_admin_login, is_admin_login, admin_check_cookie
from .models import UserInfo, TeacherInfo, CourseInfo, Teacher2Course, choose_course, AdminInfo, attendance, \
    AttendanceInfo
# from .forms import fileForm
# django自带加密解密库
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Q, Avg, Sum, Max, Min, Count
import hashlib
import json
import operator
import datetime
import smtplib
from email.mime.text import MIMEText
from Crypto.Cipher import AES
import base64
import os
import xlrd
import pytz
import simplejson
import time

from django.core.files.base import ContentFile
from django.core.files import File

import os
import cv2
import dlib

# import csv
import sys
import numpy as np
import time
from sklearn.externals import joblib
# import argparse
import os
from sklearn.ensemble import ExtraTreesClassifier
import cv2

from sklearn.model_selection import train_test_split
import tensorflow as tf
import random
from datetime import datetime

import subprocess
import paramiko

import sys
import os
import cv2
import dlib
import argparse

from PIL import Image
import random
import os
import numpy as np

import tensorflow as tf
import cv2
import numpy as np
import os
import random
import sys
from sklearn.model_selection import train_test_split

from datetime import datetime


# Create your views here.

# 检查是否登录的装饰器
# def check_login(func):
#     def inner(request,*args,**kwargs):
#         (flag, rank) = check_cookie(request)
#         if flag:
#             func(request,*args,**kwargs)
#         else:
#             return render(request, 'page-login.html', {'error_msg': ''})
#
#     return inner

# 首页
def index(request):
    return redirect('/check/')
    # (flag, rank) = check_cookie(request)
    # print('flag', flag)
    #
    # if flag:
    #     return render(request, 'check.html',locals())
    #
    # return render(request, 'page-login.html', {'error_msg': ''})


def teacher_index(request):
    return redirect('/teacher_check/')


def admin_index(request):
    return redirect('/admin_check/')


# 联系我们
@is_login
def contact_us(request):
    return render(request, 'contact_us.html')


@is_teacher_login
def teacher_contact_us(request):
    return render(request, 'teacher_contact_us.html')


# 个人信息
@is_login
def personal_details(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # print(request.POST,";")
        # print(request.POST.get)
        email = request.POST.get('email')
        stu_num = request.POST.get('stu_num')
        pwd = request.POST.get('password')
        # print(stu_num, username, email, pwd)
        secret_key = "QWqw12!@QWqw12!@"
        cipher = AES.new(secret_key, AES.MODE_ECB)  # never use ECB in strong systems obviously
        if len(pwd) < 16:  # 密码长度为6-16之间
            pwd += " " * (16 - len(pwd))
        pwd = base64.b64encode(cipher.encrypt(pwd))
        pwd = bytes.decode(pwd)
        phone = request.POST.get('phone')
        # print(stu_num, username, email, pwd, phone)
        UserInfo.objects.filter(studentNum=stu_num).update(username=username, email=email, password=pwd,
                                                           phone=phone)
        return HttpResponse('OK')
    else:
        user_email = request.COOKIES["qwer"]
        # print(request.COOKIES["qwer"])
        user = UserInfo.objects.filter(email=user_email)
        for row in user:
            studentNum = row.studentNum
            secret_key = "QWqw12!@QWqw12!@"  # 密钥
            cipher = AES.new(secret_key, AES.MODE_ECB)  # never use ECB in strong systems obviously
            decoded_password = cipher.decrypt(base64.b64decode(str.encode(row.password)))
            decoded_password = bytes.decode(decoded_password)  # bytes to str
            password = decoded_password.strip(" ")  # 正文
            username = row.username
            phone = row.phone
        return render(request, 'personal_details.html',
                      {"studentNum": studentNum, "password": password, "username": username, "phone": phone,
                       "email": user_email})


@is_teacher_login
def teacher_details(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # print(request.POST,";")
        print(request.POST.get)
        email = request.POST.get('email')
        stu_num = request.POST.get('stu_num')
        pwd = request.POST.get('password')
        # print(stu_num, username, email, pwd)
        secret_key = "QWqw12!@QWqw12!@"
        cipher = AES.new(secret_key, AES.MODE_ECB)  # never use ECB in strong systems obviously
        if len(pwd) < 16:  # 密码长度为6-16之间
            pwd += " " * (16 - len(pwd))
        pwd = base64.b64encode(cipher.encrypt(pwd))
        pwd = bytes.decode(pwd)
        phone = request.POST.get('phone')
        # print(stu_num, username, email, pwd, phone)
        TeacherInfo.objects.filter(teacherNum=stu_num).update(teacherName=username, email=email, password=pwd,
                                                              phone=phone)
        return HttpResponse("OK")
    else:
        user_email = request.COOKIES["qwer"]
        # print(request.COOKIES["qwer"])
        user = TeacherInfo.objects.filter(email=user_email)
        for row in user:
            teacherNum = row.teacherNum
            secret_key = "QWqw12!@QWqw12!@"  # 密钥
            cipher = AES.new(secret_key, AES.MODE_ECB)  # never use ECB in strong systems obviously
            decoded_password = cipher.decrypt(base64.b64decode(str.encode(row.password)))
            decoded_password = bytes.decode(decoded_password)  # bytes to str
            password = decoded_password.strip(" ")  # 正文
            teacherName = row.teacherName
            phone = row.phone
        return render(request, 'teacher_details.html',
                      {"teacherNum": teacherNum, "password": password, "teacherName": teacherName, "phone": phone,
                       "email": user_email})


# # 签到统计
# @is_login
# def total(request):
#     (flag, user) = check_cookie(request)
#     # if flag:
#     if request.method == 'POST':
#         nowdate = datetime.datetime.now()
#         weekDay = datetime.datetime.weekday(nowdate)
#         firstDay = nowdate - datetime.timedelta(days=weekDay)
#         lastDay = nowdate + datetime.timedelta(days=6 - weekDay)
#         # print(firstDay,lastDay)
#         # info_list=Attendence.objects.filter(date__gte=firstDay,date__lte=lastDay).values('stu','stu__username','stu__cid__name').annotate(total_time=Sum('duration'),leave_count=Sum('is_leave')).order_by()
#         info_list = Attendence.objects.filter(date__gte=firstDay, date__lte=lastDay).values('stu', 'stu__username',
#                                                                                             'stu__cid__name',
#                                                                                             'leave_count') \
#             .annotate(total_time=Sum('duration')).order_by()
#         info_list = json.dumps(list(info_list), cls=DecimalEncoder)
#
#         return HttpResponse(info_list)
#     else:
#         nowdate = datetime.datetime.now()
#         weekDay = datetime.datetime.weekday(nowdate)
#         firstDay = nowdate - datetime.timedelta(days=weekDay)
#         lastDay = nowdate + datetime.timedelta(days=6 - weekDay)
#         # print(firstDay,lastDay)
#         leave_list = Leave.objects.filter().values('user', 'start_time', 'end_time')
#         # print(leave_list)
#         info_list = Attendence.objects.filter(date__gte=firstDay, date__lte=lastDay).values('stu', 'stu__username',
#                                                                                             'stu__cid__name',
#                                                                                             'leave_count') \
#             .annotate(total_time=Sum('duration')).order_by()
#
#         # info_list=Attendence.objects.filter(date__gte=firstDay,date__lte=lastDay).values('stu','stu__username','stu__cid__name')\
#         #     .annotate(total_time=Sum('duration'),leave_count=Sum('is_leave'))\
#         #     .extra(
#         #     select={'starttime':"select start_time from app_leave where %s BETWEEN start_time AND end_time"},
#         #     select_params=[nowdate]
#         # )\
#         #     .order_by()
#
#         # info_list=json.dumps(list(info_list),cls=DecimalEncoder)
#         print(info_list)
#
#         return render(request, 'total.html', locals())
#     # else:
#     #     return render(request, 'page-login.html', {'error_msg': ''})


# 登录页面
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        account_rank = request.POST['account_rank']
        print("account_rank", account_rank)
        # m1 = hashlib.sha1()
        # m1.update(password.encode('utf8'))
        # password = m1.hexdigest()
        secret_key = "QWqw12!@QWqw12!@"
        cipher = AES.new(secret_key, AES.MODE_ECB)  # never use ECB in strong systems obviously
        if len(password) < 16:  # 密码长度为6-16之间
            password += " " * (16 - len(password))
        password = base64.b64encode(cipher.encrypt(password))
        password = bytes.decode(password)
        print('密码:', password)
        if account_rank == "student":
            if check_login(email, password):
                response = redirect('/index/')
                response.set_cookie('qwer', email, 3600)
                response.set_cookie('asdf', password, 3600)
                return response
                # return HttpResponse('登录成功')
            else:
                return render(request, 'page-login.html', {'error_msg': '账号密码错误或身份错误请重新输入'})
        elif account_rank == "teacher":
            if check_teacher_login(email, password):
                response = redirect('/teacher_index/')
                response.set_cookie('qwer', email, 3600)
                response.set_cookie('asdf', password, 3600)
                return response
                # return HttpResponse('登录成功')
            else:
                return render(request, 'page-login.html', {'error_msg': '账号密码错误或身份错误请重新输入'})
        else:
            if check_admin_login(email, password):
                response = redirect('/admin_index/')
                response.set_cookie('qwer', email, 3600)
                response.set_cookie('asdf', password, 3600)
                return response
                # return HttpResponse('登录成功')
            else:
                return render(request, 'page-login.html', {'error_msg': '账号密码错误或身份错误请重新输入'})
    else:
        (flag, rank) = check_cookie(request)
        print("check_cookie(request)", check_cookie(request))
        print('flag', flag)
        if flag:
            return redirect('/index/')
        return render(request, 'page-login.html', {'error_msg': ''})


@csrf_exempt
def teacher_login(request):
    (flag, rank) = teacher_check_cookie(request)
    print("check_cookie(request)", teacher_check_cookie(request))
    print('flag', flag)
    if flag:
        return redirect('/teacher_index/')
    return render(request, 'page-login.html', {'error_msg': ''})


@csrf_exempt
def admin_login(request):
    (flag, rank) = admin_check_cookie(request)
    print("check_cookie(request)", admin_check_cookie(request))
    print('flag', flag)
    if flag:
        return redirect('/admin_index/')
    return render(request, 'page-login.html', {'error_msg': ''})


# 忘记密码页面
@csrf_exempt
def forget_password(request):
    if request.method == 'POST':
        email_verify = request.POST['email_verify']
        account_rank = request.POST['account_rank']
        if account_rank == "student":
            result = UserInfo.objects.filter(email=email_verify)
        elif account_rank == "teacher":
            result = TeacherInfo.objects.filter(email=email_verify)
        else:
            result = AdminInfo.objects.filter(email=email_verify)
        if result.count() == 0:
            return_message = "请输入正确邮箱以及选中相应的用户身份"
            return render(request, 'forget_password.html', {'error_msg': return_message})
        else:
            for row in result:
                # 第三方 SMTP 服务
                msg_from = '465074419@qq.com'  # 发送方邮箱
                passwd = 'ivffmyoygykvbjcg'  # 填入发送方邮箱的授权码
                msg_to = email_verify  # 收件人邮箱
                subject = "人脸识别考勤系统找回密码\n"  # 主题
                secret_key = "QWqw12!@QWqw12!@"  # 密钥
                cipher = AES.new(secret_key, AES.MODE_ECB)  # never use ECB in strong systems obviously
                print("row.password:", str.encode(row.password))
                decoded_password = cipher.decrypt(base64.b64decode(str.encode(row.password)))  # 解密
                decoded_password = bytes.decode(decoded_password)  # bytes to str
                content = "您的密码是:" + decoded_password.strip(" ")  # 正文
                msg = MIMEText(content)
                msg['Subject'] = subject
                msg['From'] = msg_from
                msg['To'] = msg_to
                try:
                    s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
                    s.login(msg_from, passwd)
                    s.sendmail(msg_from, msg_to, msg.as_string())
                    return_message = "密码已发送至邮箱" + email_verify
                    return render(request, 'forget_password.html', {'error_msg': return_message})
                except s.SMTPException:
                    return_message = "邮件发送失败，请重新尝试"
                    return render(request, 'forget_password.html', {'error_msg': return_message})
    else:
        return render(request, 'forget_password.html')


@is_admin_login
def decode(request):
    if request.method == 'POST':
        decode = request.POST.get("decode")
        code = request.POST.get("code")
        if decode is not "":
            secret_key = "QWqw12!@QWqw12!@"
            cipher = AES.new(secret_key, AES.MODE_ECB)  # never use ECB in strong systems obviously
            if len(decode) < 16:  # 密码长度为6-16之间
                decode += " " * (16 - len(decode))
            print("decode", decode)
            print(len(decode))
            code = base64.b64encode(cipher.encrypt(decode))
            code = bytes.decode(code)
            decode = decode.strip(" ")
            return render(request, "decode.html", {"code": code, "decode": decode})
        elif code is not "":
            secret_key = "QWqw12!@QWqw12!@"  # 密钥
            cipher = AES.new(secret_key, AES.MODE_ECB)  # never use ECB in strong systems obviously
            decode = cipher.decrypt(base64.b64decode(str.encode(code)))
            decode = bytes.decode(decode)  # bytes to str
            decode = decode.strip(" ")  # 正文
            return render(request, "decode.html", {"code": code, "decode": decode})
        else:
            return render(request, "decode.html", {"code": "", "decode": ""})
    else:
        return render(request, "decode.html", {"code": "", "decode": ""})


# 注册页面
@csrf_exempt
def register(request):
    if request.method == 'POST':
        if request.is_ajax():

            stu_num_v = request.POST.get('stu_num_verify')
            if UserInfo.objects.filter(studentNum=stu_num_v):
                ret = {'valid': False}
            else:
                ret = {'valid': True}

            return HttpResponse(json.dumps(ret))

    else:
        return render(request, 'register.html')


@csrf_exempt
def course_verify(request):
    if request.method == 'POST':
        if request.is_ajax():

            cour_num_v = request.POST.get('cour_num_verify')
            email_v = request.POST.get('email_verify')

            if Teacher2Course.objects.filter(teacher_id=TeacherInfo.objects.filter(email=email_v)[0].teacherNum,
                                             course_id=cour_num_v):
                ret = {'valid': False}
            else:
                ret = {'valid': True}

            return HttpResponse(json.dumps(ret))
    else:
        return redirect("/create_course/")


@is_login
def face_upload(request):
    if request.method == 'POST':
        email = request.COOKIES["qwer"]
        mymodel = UserInfo.objects.get(email=email)
        # print(request.FILES)
        # for i in request.FILES.get('input-id'):
        #     print("i",i)
        #     break
        photo = request.FILES.getlist('input-id')
        if len(photo) is not 5:
            return render(request, 'face_upload.html', {"img_info": "请上传<5>张人脸"})
        # print(request.FILES.getlist('input-id')[0])
        # print(request.FILES.getlist('input-id')[1])
        # return HttpResponse("test")
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_path = os.path.join(BASE_DIR, "static")
        train_set_path = os.path.join(media_path, "train_set")
        final_path = os.path.join(train_set_path, mymodel.studentNum)
        if os.path.exists(final_path):
            deldir = os.listdir(final_path)
            for file in deldir:
                filePath = os.path.join(final_path, file)
                if os.path.isfile(filePath):
                    os.remove(filePath)
        else:
            os.mkdir(final_path)
        file_path = os.path.join(final_path, photo[0].name)
        print("file_path", file_path)
        f = open(file_path, "wb")
        for chunk in photo[0].chunks():
            f.write(chunk)
        f.close()
        mymodel.img1 = file_path
        file_path = os.path.join(final_path, photo[1].name)
        print("file_path", file_path)
        f = open(file_path, "wb")
        for chunk in photo[1].chunks():
            f.write(chunk)
        f.close()
        mymodel.img2 = file_path
        file_path = os.path.join(final_path, photo[2].name)
        print("file_path", file_path)
        f = open(file_path, "wb")
        for chunk in photo[2].chunks():
            f.write(chunk)
        f.close()
        mymodel.img3 = file_path
        file_path = os.path.join(final_path, photo[3].name)
        print("file_path", file_path)
        f = open(file_path, "wb")
        for chunk in photo[3].chunks():
            f.write(chunk)
        f.close()
        mymodel.img4 = file_path
        file_path = os.path.join(final_path, photo[4].name)
        print("file_path", file_path)
        f = open(file_path, "wb")
        for chunk in photo[4].chunks():
            f.write(chunk)
        f.close()
        mymodel.img5 = file_path
        mymodel.save()
        # if photo:
        # file_content = ContentFile(photo.read())  # 创建ContentFile对象
        # # file_content = File(photo.read())   #创建File对象
        # mymodel.img1.save(name=photo.name, content=file_content)  # 保存文件到user的photo域
        # i.save()
        # for i in mymodel:
        # i.img1.save(request.FILES["img1"].name,ContentFile(request.FILES["img1"].read()),save=True)

        # i.img1 = File(request.FILES["input-id"].read())
        # # print(request.FILES["input-id"])
        # # i.img1 = request.FILES["input-id"].name
        # i.name1 = request.FILES["input-id"].name
        # i.save()
        # i.img1.save(request.FILES["input-id"].name,ContentFile(request.FILES["input-id"].read()),save=True)
        # 读取上传的文件中的video项为二进制文件
        # print(request.FILES['input-id'])
        # print(request.FILES['input-id'].name)
        # print(request.FILES['input-id'].read())
        # file_content = ContentFile(request.FILES['input-id'].read())
        # ImageField的save方法，第一个参数是保存的文件名，第二个参数是ContentFile对象，里面的内容是要上传的图片、视频的二进制内容
        # print(type(request.FILES['input-id'].name))
        # print(type(str(request.FILES['input-id'].name)))
        # mymodel.img1.save(name=request.FILES['input-id'].name, content=file_content)
        return render(request, 'face_upload.html', {"img_info": "上传成功"})
    else:
        return render(request, 'face_upload.html')


# def face_upload(request):
#     # if not request.user.is_authenticated():
#     #     json = simplejson.dumps({
#     #         'success': False,
#     #         'errors': {'__all__': 'Authentication required'}})
#     #     return HttpResponse(json, mimetype='application/json')
#     if request.method == 'POST':
#         form = fileForm(request.POST or None, request.FILES or None)
#         print("request.POST",request.POST)
#         print("request.FILES", request.FILES)
#         print("request.FILES-input", request.FILES["img1"])
#         print("type",type(request.FILES["img1"]))
#         print("form",form)
#         if form.is_valid():
#             # img1 = form.save()  # 保存Form和Model
#             email = request.COOKIES["qwer"]
#             mymodel = UserInfo.objects.filter(email=email)
#             for i in mymodel:
#                 i.img1=ContentFile(request.FILES['img1'].read())
#                 print(type(ContentFile(request.FILES['img1'].read())))
#                 i.save()
#             # json = simplejson.dumps({
#             #     'success': True,
#             #     'upload': {
#             #         'links': {
#             #             'original': img1.img1.url},
#             #         'img1': {
#             #             'width': img1.img1.width,
#             #             'height': img1.img1.height}
#             #     }
#             # })
#             return HttpResponse("OK")
#         else:
#             json = simplejson.dumps({
#                 'success': False, 'errors': form.errors})
#             return HttpResponse(json)
#         # return HttpResponse(json, mimetype='application/json')
#
#     else:
#         return render(request, 'face_upload.html')

def imgSplit(img):
    img_split = img.split("/")
    print("img_split", img_split)
    img_src = ""
    for i in range(len(img_split)):
        if i <= 3:
            continue
        else:
            img_src = img_src + "/" + img_split[i]
    print(img_src)
    return img_src


@is_login
def face_gallery(request):
    email = request.COOKIES["qwer"]
    mymodel = UserInfo.objects.get(email=email)
    img1 = imgSplit(mymodel.img1)
    img1_name = img1.split("/")[-1]
    print(img1_name)
    img2 = imgSplit(mymodel.img2)
    img2_name = img2.split("/")[-1]
    img3 = imgSplit(mymodel.img3)
    img3_name = img3.split("/")[-1]
    img4 = imgSplit(mymodel.img4)
    img4_name = img4.split("/")[-1]
    img5 = imgSplit(mymodel.img5)
    img5_name = img5.split("/")[-1]
    return render(request, "face_gallery.html",
                  {"img1": img1, "img2": img2, "img3": img3, "img4": img4, "img5": img5, "img1_name": img1_name,
                   "img2_name": img2_name, "img3_name": img3_name, "img4_name": img4_name, "img5_name": img5_name})


def check(request):
    (flag, rank) = check_cookie(request)
    # print('flag', flag)
    user = rank

    if flag:
        #         if request.method == 'POST':
        #             sign_flag = request.POST.get('sign')
        #             print('sign_flag', type(sign_flag), sign_flag)
        #             if sign_flag == 'True':
        #                 Attendence.objects.create(stu=user, start_time=datetime.datetime.now())
        #             elif sign_flag == 'False':
        #                 cur_attendent = Attendence.objects.filter(stu=user, end_time=None)
        #                 tmp_time = datetime.datetime.now()
        #                 duration = round((tmp_time - cur_attendent.last().start_time).seconds / 3600, 1)
        #
        #                 cur_attendent.update(end_time=tmp_time, duration=duration)
        #             return HttpResponse(request, '操作成功')
        #         else:
        #             # 查询上一个签到的状态
        #             pre_att = Attendence.objects.filter(stu=user).order_by('id').last()
        #             # print(pre_att.end_time)
        #             if pre_att:
        #                 # 如果当前时间距上次签到时间超过六小时，并且上次签退时间等于签到时间
        #                 if (datetime.datetime.now() - pre_att.start_time.replace(
        #                         tzinfo=None)).seconds / 3600 > 6 and pre_att.end_time == None:
        #                     # Attendence.objects.filter(stu=user, end_time=None).update(end_time=pre_att.start_time+datetime.timedelta(hours=2),duration=2,detail="自动签退")
        #                     pre_att.delete()
        #                     sign_flag = True
        #
        #                 elif (datetime.datetime.now() - pre_att.start_time.replace(
        #                         tzinfo=None)).seconds / 3600 < 6 and pre_att.end_time == None:
        #                     sign_flag = False
        #                 else:
        #                     sign_flag = True
        #             else:
        #                 sign_flag = True
        #             att_list = Attendence.objects.all().order_by('-id')
        #
        return render(request, 'check.html', locals())
    #
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


def teacher_check(request):
    (flag, rank) = teacher_check_cookie(request)
    # print('flag', flag)
    user = rank
    if flag:
        return render(request, 'teacher_check.html', locals())
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


def admin_check(request):
    (flag, rank) = admin_check_cookie(request)
    # print('flag', flag)
    user = rank
    if flag:
        return render(request, 'admin_check.html', locals())
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


#

# 注销登录
def logout(request):
    req = redirect('/login/')
    req.delete_cookie('asdf')
    req.delete_cookie('qwer')
    return req


# 注册验证
def register_verify(request):
    if request.method == 'POST':
        print('验证成功')
        username = request.POST.get('username')
        email = request.POST.get('email')
        stu_num = request.POST.get('stu_num')
        pwd = request.POST.get('password')
        # m1 = hashlib.sha1()
        # m1.update(pwd.encode('utf8'))
        # pwd = m1.hexdigest()
        secret_key = "QWqw12!@QWqw12!@"
        cipher = AES.new(secret_key, AES.MODE_ECB)  # never use ECB in strong systems obviously
        if len(pwd) < 16:  # 密码长度为6-16之间
            pwd += " " * (16 - len(pwd))
        pwd = base64.b64encode(cipher.encrypt(pwd))
        pwd = bytes.decode(pwd)
        phone = request.POST.get('phone')
        a = UserInfo.objects.create(username=username, email=email, studentNum=stu_num, password=pwd,
                                    phone=phone)

        a.save()
        return HttpResponse('OK')


# # 班级管理
# def classManage(request):
#     (flag, rank) = check_cookie(request)
#     print('flag', flag)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             class_list = ClassInfo.objects.all()
#
#             return render(request, 'classManage.html', {'class_list': class_list})
#         else:
#             return render(request, 'class_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})


# # 编辑班级
# @csrf_exempt
# def edit_class(request):
#     (flag, rank) = check_cookie(request)
#     print('flag', flag)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             if request.method == 'POST':
#                 pre_edit_id = request.POST.get('edit_id')
#                 class_name = request.POST.get('edit_class_name')
#                 temp_flag = ClassInfo.objects.filter(name=class_name)
#                 print('pre_edit_id1', pre_edit_id)
#                 pre_obj = ClassInfo.objects.get(id=pre_edit_id)
#                 if not temp_flag and class_name:
#                     pre_obj.name = class_name
#                     pre_obj.save()
#                 return HttpResponse('班级修改成功')
#             class_list = ClassInfo.objects.all()
#             return render(request, 'classManage.html', {'class_list': class_list})
#             # return HttpResponse('编辑班级')
#         else:
#             return render(request, 'class_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})


# # 添加班级
# @csrf_exempt
# def add_class(request):
#     # print('进来了')
#     if request.method == 'POST':
#         # print('这是post')
#         add_class_name = request.POST.get('add_class_name')
#         flag = ClassInfo.objects.filter(name=add_class_name)
#         if flag:
#             pass
#             # print('已有数据，不处理')
#         else:
#             if add_class_name:
#                 ClassInfo.objects.create(name=add_class_name).save()
#
#         return HttpResponse('添加班级成功')

#
# # 删除班级
# def delete_class(request):
#     (flag, rank) = check_cookie(request)
#     print('flag', flag)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             # class_list=ClassInfo.objects.all()
#             delete_id = request.GET.get('delete_id')
#             ClassInfo.objects.filter(id=delete_id).delete()
#             return redirect('/classManage/')
#         else:
#             return render(request, 'class_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})


# # 专业管理
# def majorManage(request):
#     (flag, rank) = check_cookie(request)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             major_list = MajorInfo.objects.all()
#
#             return render(request, 'major_manage.html', {'major_list': major_list})
#         else:
#             return render(request, 'major_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})


# # 添加专业
# @csrf_exempt
# def add_major(request):
#     (flag, rank) = check_cookie(request)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             major_list = MajorInfo.objects.all()
#             if request.method == 'POST':
#
#                 add_major_name = request.POST.get('add_major_name')
#                 print(add_major_name)
#                 if not MajorInfo.objects.filter(name=add_major_name):
#                     new_major = MajorInfo.objects.create(name=add_major_name)
#                 return HttpResponse('专业添加成功')
#
#             return render(request, 'major_manage.html', {'major_list': major_list})
#         else:
#             return render(request, 'major_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})
#
#
# # 删除专业
# def delete_major(request):
#     (flag, rank) = check_cookie(request)
#     if flag:
#         if rank.user_type.caption == 'admin':
#
#             delete_major_id = request.GET.get('delete_id')
#             MajorInfo.objects.get(id=delete_major_id).delete()
#             major_list = MajorInfo.objects.all()
#             return render(request, 'major_manage.html', {'major_list': major_list})
#         else:
#             return render(request, 'major_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})
#
#
# # 编辑专业
# @csrf_exempt
# def edit_major(request):
#     (flag, rank) = check_cookie(request)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             major_list = MajorInfo.objects.all()
#             edit_major_id = request.POST.get('edit_major_id')
#             edit_major_name = request.POST.get('edit_major_name')
#             print(edit_major_id)
#             print(edit_major_name)
#             if not MajorInfo.objects.filter(name=edit_major_name):
#                 change_obj = MajorInfo.objects.get(id=edit_major_id)
#                 change_obj.name = edit_major_name
#                 change_obj.save()
#             return HttpResponse('专业修改成功')
#
#         else:
#             return render(request, 'major_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})
#
#
# # 成员管理
# def member_manage(request):
#     (flag, rank) = check_cookie(request)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             member_list = UserInfo.objects.all()
#
#             return render(request, 'member_manage.html', {'member_list': member_list})
#         else:
#             return render(request, 'member_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})


# 删除成员
def delete_member(request):
    (flag, rank) = check_cookie(request)
    if flag:
        if rank.user_type.caption == 'admin':
            delete_sno = request.GET.get('delete_sno')
            UserInfo.objects.get(studentNum=delete_sno).delete()
            member_list = UserInfo.objects.all()
            return render(request, 'member_manage.html', {'member_list': member_list})
        else:
            return render(request, 'member_manage_denied.html')
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


# #   编辑成员
# def edit_member(request):
#     (flag, rank) = check_cookie(request)
#     if flag:
#         if rank.user_type.caption == 'admin':
#
#             if request.method == 'POST':
#                 student_num = request.POST.get('student_num')
#                 username = request.POST.get('username')
#                 email = request.POST.get('email')
#                 age = request.POST.get('age')
#                 if age:
#                     age = int(age)
#                 else:
#                     age = 0
#
#                 gender = int(request.POST.get('gender'))
#                 cls = ClassInfo.objects.get(name=request.POST.get('cls'))
#                 nickname = request.POST.get('nickname')
#                 usertype = UserType.objects.get(caption=request.POST.get('user_type'))
#                 phone = request.POST.get('phone')
#                 motto = request.POST.get('motto')
#                 edit_obj = UserInfo.objects.filter(studentNum=student_num)
#                 edit_obj.update(studentNum=student_num, username=username, email=email, cid=cls, nickname=nickname,
#                                 user_type=usertype, motto=motto,
#                                 gender=gender, phone=phone,
#                                 age=age
#                                 )
#                 member_list = UserInfo.objects.all()
#
#                 return redirect('/memberManage/', {'member_list': member_list})
#             else:
#                 edit_member_id = request.GET.get('edit_sno')
#                 # 所有用户类型列表
#                 stu_type_list = UserType.objects.all()
#                 # 所有的班级
#                 cls_list = ClassInfo.objects.all()
#                 # 所有的专业
#                 major_list = MajorInfo.objects.all()
#                 # 当前编辑的用户对象
#                 edit_stu_obj = UserInfo.objects.get(studentNum=edit_member_id)
#                 return render(request, 'edit_member.html', locals())
#         else:
#             return render(request, 'member_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})


# # 公告墙展示
# @is_login
# def notice(request):
#     info_list = Notice.objects.all().order_by('-post_date')
#     return render(request, 'notice.html', locals())


# # 公告墙发布
# @is_login
# def noticeManage(request):
#     (flag, user) = check_cookie(request)
#     if user.user_type.caption == 'admin':
#         if request.method == 'POST':
#             title = request.POST.get('title')
#             content = request.POST.get('content')
#             level = request.POST.get('selectLevel')
#             Notice.objects.create(head=title, content=content, level=level, author=user)
#             return render(request, 'notice_manage.html')
#         else:
#             return render(request, 'notice_manage.html')
#     else:
#         return render(request, 'notice_manage_denied.html')
#

# 请假管理
# @is_login
# def leave(request):
#     (flag, user) = check_cookie(request)
#     leave_list = Leave.objects.all()
#     if request.method == 'POST':
#         starttime = request.POST.get('starttime')
#         endtime = request.POST.get('endtime')
#         print(starttime)
#         a = int(datetime.datetime.strptime(starttime, '%Y-%m-%d').day - datetime.datetime.strptime(endtime,
#                                                                                                    '%Y-%m-%d').day) + 1
#         explain = request.POST.get('explain')
#         Leave.objects.create(start_time=starttime, end_time=endtime, user=user, explain=explain)
#         Attendence.objects.filter(date__gte=starttime, date__lte=endtime, stu=user).update(
#             leave_count=F('leave_count') + a)
#     return render(request, 'leave.html', locals())


# # 考核记录
# @is_login
# def exam(request):
#     exam_list = ExamContent.objects.all()
#     exam_id = request.GET.get('exam_id')
#     if exam_id:
#         user_list = Exam.objects.filter(content_id=exam_id).all()
#     return render(request, 'exam.html', locals())

#
# # 考核管理
# @is_login
# def exam_manage(request):
#     (flag, user) = check_cookie(request)
#     if user.user_type.caption == 'admin':
#         if request.method == 'POST':
#             title = request.POST.get('title')
#
#             if title:
#                 ExamContent.objects.create(title=title)
#             else:
#                 count = UserInfo.objects.all().count()
#                 content_id = request.POST.get('exam_id')
#                 for i in range(count):
#                     point = request.POST.get('point{}'.format(i))
#
#                     stuID = request.POST.get('stu{}'.format(i))
#                     detail = request.POST.get('detail{}'.format(i))
#                     Exam.objects.create(point=point, content_id=content_id, user_id=stuID, detail=detail)
#                 # print(request.body)
#                 ExamContent.objects.filter(id=content_id).update(state=True)
#         check_list = ExamContent.objects.filter(state=False)
#         user_list = UserInfo.objects.all()
#         return render(request, 'exam_manage.html', locals())
#     else:
#         return render(request, 'exam_manage_denied.html')
@is_teacher_login
def create_course(request):
    email = request.COOKIES["qwer"]
    teacher_model = TeacherInfo.objects.get(email=email)
    teacherNum = teacher_model.teacherNum
    if request.method == 'POST':
        courseId = request.POST.get('course_id')
        courseName = request.POST.get('course_name')
        if CourseInfo.objects.filter(courseNum=courseId, courseName=courseName):
            pass
        else:
            a = CourseInfo.objects.create(courseNum=courseId, courseName=courseName)
            a.save()

        b = Teacher2Course.objects.create(teacher_id=TeacherInfo.objects.get(teacherNum=teacherNum),
                                          course_id=CourseInfo.objects.get(courseNum=courseId))
        b.save()
        return redirect("/create_course/")
    else:
        courses = Teacher2Course.objects.filter(teacher_id=teacherNum)
        print(courses)
        for i in courses:
            print(i.course_id.courseNum)
        return render(request, "create_course.html", {"courses": courses, "email": email})


@is_admin_login
def operation(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, "operation.html")


@is_admin_login
def add_UserInfo_2db(request):
    if request.method == 'POST':

        xml_file = request.FILES.get('file_name')
        print("文件后缀", os.path.splitext(xml_file.name)[1])
        if (os.path.splitext(xml_file.name)[1] == '.xls'):
            pass
        else:
            return redirect("/operation/")
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_path = os.path.join(BASE_DIR, "static")
        uploads_path = os.path.join(media_path, "uploads")
        final_path = os.path.join(uploads_path, xml_file.name)
        if os.path.exists(final_path):
            os.remove(final_path)
        f = open(final_path, "wb")
        for chunk in xml_file.chunks():
            f.write(chunk)
        f.close()

        workbook = xlrd.open_workbook(final_path)
        # workbook = xlrd.open_workbook(r'/root/zlf_projects/pycharm_project_48/UserInfo.xls')
        print(workbook.sheet_names())  # 查看所有sheet名称
        sheet1 = workbook.sheet_by_index(0)  # 用索引取第1个sheet

        cell_00 = sheet1.cell_value(0, 0)  # 读取第1行第1列数据
        row0 = sheet1.row_values(0)  # 读取第1行数据
        nrows = sheet1.nrows  # 读取行数
        print(cell_00, row0, nrows)

        for i in range(nrows):  # 循环逐行打印
            if i == 0:  # 跳过第一行，标题
                continue
            print(sheet1.row_values(i)[:5])  # 取前5列
            a = UserInfo.objects.create(studentNum=str(int(sheet1.row_values(i)[0])), password=sheet1.row_values(i)[1],
                                        username=sheet1.row_values(i)[2],
                                        phone=str(int(sheet1.row_values(i)[3])), email=sheet1.row_values(i)[4])

            a.save()
        return render(request, "operation.html", {"success": "提交学生用户数据成功"})
    else:
        return redirect("/operation/")


@is_admin_login
def add_UserInfo_img_2db(request):
    if request.method == 'POST':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_path = os.path.join(BASE_DIR, "static")
        train_set_dir = os.path.join(media_path, "train_set")
        print("train_set_dir", train_set_dir)
        # train_set_dir = '/root/zlf_projects/pycharm_project_48/static/train_set'
        models = UserInfo.objects.filter()
        # print(models)
        for row in models:
            # print(row)
            # print(row.studentNum)
            person_dir = os.path.join(train_set_dir, row.studentNum)
            # print("person_dir", person_dir)
            imgs = os.listdir(person_dir)
            # print("imgs", imgs)
            img1 = os.path.join(person_dir, imgs[0])
            img2 = os.path.join(person_dir, imgs[1])
            img3 = os.path.join(person_dir, imgs[2])
            img4 = os.path.join(person_dir, imgs[3])
            img5 = os.path.join(person_dir, imgs[4])
            print(img1, img2, img3, img4, img5)
            UserInfo.objects.filter(studentNum=row.studentNum).update(img1=img1, img2=img2, img3=img3, img4=img4,
                                                                      img5=img5)
        return render(request, "operation.html", {"success": "提交学生用户人脸成功"})
    else:
        return redirect("/operation/")


@is_teacher_login
def student2course_connection(request):
    if request.method == 'POST':
        email = request.COOKIES["qwer"]
        teacher_model = TeacherInfo.objects.get(email=email)
        courseNum = request.POST.get('courseNum')
        # print("num",num)
        # print(request.FILES)
        xml_file = request.FILES.get('file_name')
        print("文件后缀", os.path.splitext(xml_file.name)[1])
        if (os.path.splitext(xml_file.name)[1] == '.xls'):
            pass
        else:
            return redirect("/create_course/")
        # print(xml_file)
        # print(xml_file.name)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_path = os.path.join(BASE_DIR, "static")
        uploads_path = os.path.join(media_path, "uploads")
        final_path = os.path.join(uploads_path, xml_file.name)
        if os.path.exists(final_path):
            os.remove(final_path)
        f = open(final_path, "wb")
        for chunk in xml_file.chunks():
            f.write(chunk)
        f.close()

        workbook = xlrd.open_workbook(final_path)
        print(workbook.sheet_names())  # 查看所有sheet名称
        sheet1 = workbook.sheet_by_index(0)  # 用索引取第1个sheet

        # cell_00 = sheet1.cell_value(0, 0)  # 读取第1行第1列数据
        # row0 = sheet1.row_values(0)  # 读取第1行数据
        nrows = sheet1.nrows  # 读取行数
        # print(cell_00, row0, nrows)

        for i in range(nrows):  # 循环逐行打印
            if i == 0:  # 跳过第一行，标题
                continue
            # print(sheet1.row_values(i)[:5])  # 取前5列
            a = choose_course.objects.create(stu=UserInfo.objects.get(studentNum=str(int(sheet1.row_values(i)[0]))),
                                             teac=teacher_model,
                                             cour=CourseInfo.objects.get(courseNum=courseNum))
            a.save()
        return redirect("/create_course/")
    else:
        return redirect("/create_course/")


@is_login
def chosen_course(request):
    email = request.COOKIES["qwer"]
    student_model = UserInfo.objects.get(email=email)
    course_teacher = choose_course.objects.filter(stu=student_model)
    # print("course_teacher.teac", course_teacher.teac)
    # print("course_teacher.cour", course_teacher.cour)
    teacher_course_info = []
    for row in course_teacher:
        print("row", row)
        teacher_course_info.append([TeacherInfo.objects.get(teacherNum=row.teac.teacherNum),
                                    CourseInfo.objects.get(courseNum=row.cour.courseNum)])
        print("teacher_course_info", teacher_course_info)
    return render(request, "chosen_course.html",
                  {"teacher_course_info": teacher_course_info})


@is_teacher_login
def watch_students(request):
    if request.method == 'POST':
        courseNum = request.POST.get("courseNum")
        email = request.COOKIES["qwer"]
        teacher_model = TeacherInfo.objects.get(email=email)
        course_model = CourseInfo.objects.get(courseNum=courseNum)
        results = choose_course.objects.filter(cour=course_model, teac=teacher_model)
        # print("results", results)
        # results_2 = choose_course.objects.filter(cour=course_model).filter(teac=teacher_model)
        # print("results_2", results_2)
        # for row in results:
        #     print(row)
        #     print(row.stu)
        #     print(row.stu.username)
        #     print(row.stu.img1)
        return render(request, "watch_students.html", {"results": results, "courseNum": courseNum})
    else:
        return redirect("/create_course/")


# @is_teacher_login
# def search_student_face(request):
#     if request.method == 'POST':
#         studentNum = request.POST.get("studentNum")
#         mymodel = UserInfo.objects.get(studentNum=studentNum)
#         img = imgSplit(mymodel.img1)
#         img_name = "/" + img.split("/")[-4] + "/" + img.split("/")[-3] + "/" + img.split("/")[-2] + "/" + \
#                    img.split("/")[-1]
#         print("img_name", img_name)
#         render(request, "human_face.html", {"img": img_name})
#         return render(request, "watch_students.html")
#     else:
#         render(request, "human_face.html", {"img": "/static/img/nothing.png"})
#         return render(request, "watch_students.html")
#
# @is_teacher_login
# def human_face(request):
#     return render(request, "human_face.html", {"img":"/static/img/nothing.png"})


@is_teacher_login
def watch_face(request):
    if request.method == 'POST':
        stu_face = request.POST.get("stu_face")
        stu_name = request.POST.get("stu_name")
        stu_id = request.POST.get("stu_id")
        return render(request, "watch_face.html", {"stu_face": stu_face, "stu_name": stu_name, "stu_id": stu_id})
    else:
        return redirect("/create_course/")


@is_teacher_login
def teacher_manage_atten(request):
    email = request.COOKIES["qwer"]
    teacher_model = TeacherInfo.objects.get(email=email)
    teacherNum = teacher_model.teacherNum
    if request.method == 'POST':
        course_id = request.POST.get("courseNum")
        atten_infos = AttendanceInfo.objects.filter(teacher_id=teacherNum, course_id=course_id)
        return render(request, "teacher_atten_course.html", {"atten_infos": atten_infos})
    else:
        courses = Teacher2Course.objects.filter(teacher_id=teacherNum)
        print(courses)
        for i in courses:
            print(i.course_id.courseNum)
        return render(request, "teacher_manage_atten.html", {"courses": courses})


@is_teacher_login
def teacher_atten_course(request):
    email = request.COOKIES["qwer"]
    teacher_model = TeacherInfo.objects.get(email=email)
    teacherNum = teacher_model.teacherNum
    if request.method == 'POST':
        attendance_id = request.POST.get("attendance_id")
        atten_info = attendance.objects.filter(att_id=attendance_id)
        return render(request, "teacher_atten_student.html", {"atten_info": atten_info})
    else:
        courses = Teacher2Course.objects.filter(teacher_id=teacherNum)
        print(courses)
        for i in courses:
            print(i.course_id.courseNum)
        return render(request, "teacher_manage_atten.html", {"courses": courses})


@csrf_exempt
def stu_upload(request):
    print("request: ", request)
    if request.method == 'POST':
        photo1 = request.FILES.getlist('img1')
        photo2 = request.FILES.getlist('img2')
        photo3 = request.FILES.getlist('img3')
        id = request.POST.get('id')
        print("id", id)
        atten_id = request.POST.get('atten_id')
        print("atten_id", atten_id)
        print("name1", photo1[0].name)
        print("name2", photo2[0].name)
        print("name3", photo3[0].name)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_path = os.path.join(BASE_DIR, "static")
        middle_path = os.path.join(media_path, "upload_face_from_android")

        final_path = os.path.join(middle_path, id)
        if os.path.exists(final_path):
            pass
        else:
            os.mkdir(final_path)

        file_path_1 = os.path.join(final_path, photo1[0].name)
        print("file_path_1", file_path_1)
        f = open(file_path_1, "wb")
        for chunk in photo1[0].chunks():
            f.write(chunk)
        f.close()

        file_path_2 = os.path.join(final_path, photo2[0].name)
        print("file_path_2", file_path_2)
        f = open(file_path_2, "wb")
        for chunk in photo2[0].chunks():
            f.write(chunk)
        f.close()

        file_path_3 = os.path.join(final_path, photo3[0].name)
        print("file_path_3", file_path_3)
        f = open(file_path_3, "wb")
        for chunk in photo3[0].chunks():
            f.write(chunk)
        f.close()

        attendance.objects.filter(id=atten_id).update(img1=file_path_1, img2=file_path_2, img3=file_path_3)

        return HttpResponse("200")

    else:
        return redirect('/check/')


@is_admin_login
def upload_atten_demo(request):
    if request.method == 'POST':
        teacher_id = request.POST.get("teacher_id")
        course_id = request.POST.get("course_id")
        attendance_id = AttendanceInfo.objects.filter(course_id=CourseInfo.objects.filter(courseNum=course_id)[0],
                                                      teacher_id=TeacherInfo.objects.filter(teacherNum=teacher_id)[0],
                                                      attendance_tag="1")[0]
        print("attendance_id:", attendance_id)
        students = choose_course.objects.filter(teac=TeacherInfo.objects.filter(teacherNum=teacher_id)[0],
                                                cour=CourseInfo.objects.filter(courseNum=course_id)[0])

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_path = os.path.join(BASE_DIR, "static")
        train_set_dir = os.path.join(media_path, "upload_face_from_android")

        for row in students:
            person_dir = os.path.join(train_set_dir, row.stu.studentNum)
            # print("person_dir", person_dir)
            imgs = os.listdir(person_dir)
            # print("imgs", imgs)
            img1 = os.path.join(person_dir, imgs[0])
            img2 = os.path.join(person_dir, imgs[1])
            img3 = os.path.join(person_dir, imgs[2])

            if (random.random() > 0.9):
                a = attendance.objects.create(stu=row.stu, att=attendance_id, dbm=round(random.randint(-200, -75)),
                                              tag="0",
                                              attendance_time=time.strftime('%Y-%m-%d %H:%M:%S',
                                                                            time.localtime(time.time())), img1=img1,
                                              img2=img2, img3=img3)

                a.save()
                continue
            a = attendance.objects.create(stu=row.stu, att=attendance_id, dbm=round(random.gauss(-55, 15)), tag="0",
                                          attendance_time=time.strftime('%Y-%m-%d %H:%M:%S',
                                                                        time.localtime(time.time())), img1=img1,
                                          img2=img2, img3=img3)

            a.save()
            # row.stu.studentNum
        return render(request, "operation.html", {"success": "提交考勤演示数据成功"})
    else:
        return redirect("/operation/")


# time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


@is_admin_login
def create_two_teachers(request):
    if request.method == 'POST':
        xml_file = request.FILES.get('file_name')  # 获取前端传来的文件
        print("文件后缀", os.path.splitext(xml_file.name)[1])
        if (os.path.splitext(xml_file.name)[1] == '.xls'):
            pass
        else:
            return redirect("/operation/")
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_path = os.path.join(BASE_DIR, "static")
        uploads_path = os.path.join(media_path, "uploads")
        final_path = os.path.join(uploads_path, xml_file.name)  # 得到新建表的绝对路径
        if os.path.exists(final_path):
            os.remove(final_path)
        f = open(final_path, "wb")  # 打开表，并授予写入的权限
        for chunk in xml_file.chunks():
            f.write(chunk)  # 按块写入数据
        f.close()

        workbook = xlrd.open_workbook(final_path)  # 打开新表
        print(workbook.sheet_names())  # 查看所有sheet名称
        sheet1 = workbook.sheet_by_index(0)  # 用索引取第1个sheet

        # cell_00 = sheet1.cell_value(0, 0)  # 读取第1行第1列数据
        # row0 = sheet1.row_values(0)  # 读取第1行数据
        nrows = sheet1.nrows  # 读取行数
        # print(cell_00, row0, nrows)

        for i in range(nrows):  # 循环逐行打印
            if i == 0:  # 跳过第一行，标题
                continue
            print(sheet1.row_values(i)[:5])  # 取前5列
            print(str(int(sheet1.row_values(i)[0])))  # 将值转换为字符串类型
            a = TeacherInfo.objects.create(teacherNum=str(int(sheet1.row_values(i)[0])),
                                           password=sheet1.row_values(i)[1],
                                           teacherName=sheet1.row_values(i)[2],
                                           phone=str(int(sheet1.row_values(i)[3])),
                                           email=sheet1.row_values(i)[4])
            a.save()
        return render(request, "operation.html", {"success": "创建教师用户数据成功"})
    else:
        return redirect("/operation/")


# Neiz5WXbTTFKNcMkYMgFFg==

def resize_image_process(input_dir, output_dir):
    size = 64
    # 使用dlib自带的frontal_face_detector作为我们的特征提取器
    detector = dlib.get_frontal_face_detector()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for dir in os.listdir(input_dir):

        new_path = output_dir + "/" + dir
        isExists = os.path.exists(new_path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(new_path)

            print(new_path + ' 创建成功')
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(new_path + ' 目录已存在')
            continue

        # next_dir = input_dir + "/" + dir
        # for (next_path, next_dirnames, next_filenames) in os.walk(next_dir):
        #     print("next_filenames", next_filenames)
        #     for filename in next_filenames:
        #         if filename.endswith('.bmp') or filename.endswith('.BMP') or filename.endswith('.PNG') or filename.endswith('.png') or filename.endswith('.JPG') or filename.endswith('.jpg'):
        #             picture_name = os.path.basename(filename) #获取当前文件名
        #             print('Being processed picture %s' % picture_name)
        #             img_path = next_path+'/'+filename
        #             # 从文件读取图片
        #             img = cv2.imread(img_path)
        #
        #             face = cv2.resize(img, (size, size))
        #             # 保存图片
        #             cv2.imwrite(new_path+'/'+picture_name, face)
        next_dir = input_dir + "/" + dir
        for (next_path, next_dirnames, next_filenames) in os.walk(next_dir):
            print("next_filenames", next_filenames)
            for filename in next_filenames:
                if filename.endswith('.bmp') or filename.endswith('.BMP') or filename.endswith(
                        '.PNG') or filename.endswith('.png') or filename.endswith('.JPG') or filename.endswith('.jpg'):
                    picture_name = os.path.basename(filename)  # 获取当前文件名
                    print('Being processed picture %s' % picture_name)
                    img_path = next_path + '/' + filename
                    # 从文件读取图片
                    img = cv2.imread(img_path)
                    # 转为灰度图片
                    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # 使用detector进行人脸检测 dets为返回的结果
                    dets = detector(gray_img, 1)

                    # 使用enumerate 函数遍历序列中的元素以及它们的下标
                    # 下标i即为人脸序号
                    # left：人脸左边距离图片左边界的距离 ；right：人脸右边距离图片左边界的距离
                    # top：人脸上边距离图片上边界的距离 ；bottom：人脸下边距离图片上边界的距离
                    for i, d in enumerate(dets):
                        x1 = d.top() if d.top() > 0 else 0
                        y1 = d.bottom() if d.bottom() > 0 else 0
                        x2 = d.left() if d.left() > 0 else 0
                        y2 = d.right() if d.right() > 0 else 0
                        # img[y:y+h,x:x+w]
                        face = img[x1:y1, x2:y2]
                        # 调整图片的尺寸
                        face = cv2.resize(face, (size, size))
                        # cv2.imshow('image', face)
                        # 保存图片
                        cv2.imwrite(new_path + '/' + picture_name, face)
                    # key = cv2.waitKey(30) & 0xff
                    # if key == 27:
                    # sys.exit(0)


# 预处理防伪数据集
@is_admin_login
def anti_proof_dataset(request):
    if request.method == 'POST':
        # # 使用dlib自带的frontal_face_detector作为我们的特征提取器
        # detector = dlib.get_frontal_face_detector()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_path = os.path.join(BASE_DIR, "static")
        media_path2 = os.path.join(media_path, "anti_proof_dataset")
        media_path3 = os.path.join(media_path2, "dataset")
        input_dir = os.path.join(media_path3, "ClientFace")
        media_path4 = os.path.join(media_path2, "dataset_processed")
        output_dir = os.path.join(media_path4, "ClientFace")
        # input_dir = "../dataset/ClientFace"
        # output_dir = "../dataset_processed/ClientFace"
        resize_image_process(input_dir, output_dir)

        input_dir = os.path.join(media_path3, "ImposterFace")
        output_dir = os.path.join(media_path4, "ImposterFace")
        # input_dir = "../dataset/ImposterFace"
        # output_dir = "../dataset_processed/ImposterFace"
        resize_image_process(input_dir, output_dir)

        print("[INFO]end of processing resize_image_process")
        return render(request, "operation.html", {"success": "预处理防伪图片集成功"})
    else:
        return redirect("/operation/")


# 这里开始防伪卷积神经网络
def weightVariable(shape):
    init = tf.random_normal(shape, stddev=0.01)
    return tf.Variable(init)


def biasVariable(shape):
    init = tf.random_normal(shape)
    return tf.Variable(init)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def maxPool(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def dropout(x, keep):
    return tf.nn.dropout(x, keep)


def cnnLayer(x, keep_prob_5, keep_prob_75, faces_number):
    # 第一层
    # W1 = weightVariable([3,3,3,32]) # 卷积核大小(3,3)， 输入通道(3)， 输出通道(32)
    W1 = tf.get_variable("W1", shape=[3, 3, 3, 32], initializer=tf.random_normal_initializer(stddev=0.01))
    # b1 = biasVariable([32])
    b1 = tf.get_variable("b1", shape=[32], initializer=tf.random_normal_initializer)
    # 卷积
    conv1 = tf.nn.relu(conv2d(x, W1) + b1)
    # 池化
    pool1 = maxPool(conv1)
    # 减少过拟合，随机让某些权重不更新
    drop1 = dropout(pool1, keep_prob_5)

    # 第二层
    # W2 = weightVariable([3,3,32,64])
    W2 = tf.get_variable("W2", shape=[3, 3, 32, 64], initializer=tf.random_normal_initializer(stddev=0.01))
    # b2 = biasVariable([64])
    b2 = tf.get_variable("b2", shape=[64], initializer=tf.random_normal_initializer)
    conv2 = tf.nn.relu(conv2d(drop1, W2) + b2)
    pool2 = maxPool(conv2)
    drop2 = dropout(pool2, keep_prob_5)

    # 第三层
    # W3 = weightVariable([3,3,64,64])
    W3 = tf.get_variable("W3", shape=[3, 3, 64, 64], initializer=tf.random_normal_initializer(stddev=0.01))
    # b3 = biasVariable([64])
    b3 = tf.get_variable("b3", shape=[64], initializer=tf.random_normal_initializer)
    conv3 = tf.nn.relu(conv2d(drop2, W3) + b3)
    pool3 = maxPool(conv3)
    drop3 = dropout(pool3, keep_prob_5)

    # 全连接层
    # Wf = weightVariable([8*8*64, 512])
    Wf = tf.get_variable("Wf", shape=[8 * 8 * 64, 512], initializer=tf.random_normal_initializer(stddev=0.01))
    # bf = biasVariable([512])
    bf = tf.get_variable("bf", shape=[512], initializer=tf.random_normal_initializer)
    drop3_flat = tf.reshape(drop3, [-1, 8 * 8 * 64])
    dense = tf.nn.relu(tf.matmul(drop3_flat, Wf) + bf)
    dropf = dropout(dense, keep_prob_75)

    # 输出层
    # Wout = weightVariable([512, 2])
    Wout = tf.get_variable("Wout", shape=[512, faces_number], initializer=tf.random_normal_initializer(stddev=0.01))
    # bout = biasVariable([2])
    bout = tf.get_variable("bout", shape=[faces_number], initializer=tf.random_normal_initializer)
    # out = tf.matmul(dropf, Wout) + bout
    out = tf.add(tf.matmul(dropf, Wout), bout)
    return out


# 输出层个数根据标签决定
def cnnTrain(num_batch, x, y_, keep_prob_5, keep_prob_75, inc_v1, TIMESTAMP, train_x, test_x, train_y, test_y,
             batch_size, faces_number):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media_path = os.path.join(BASE_DIR, "static")
    media_path2 = os.path.join(media_path, "anti_proof_dataset")
    tmp_path = os.path.join(media_path2, "tmp")
    out = cnnLayer(x, keep_prob_5, keep_prob_75, faces_number)

    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=out, labels=y_))
    # learning rate = 0.01
    train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)
    # 比较标签是否相等，再求的所有数的平均值，tf.cast(强制转换类型)
    # accuracy = tf.reduce_mean(tf.cast(tf.equal(out, y_), tf.float32))
    accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(out, 1), tf.argmax(y_, 1)), tf.float32))
    # 将loss与accuracy保存以供tensorboard使用
    tf.summary.scalar('loss', cross_entropy)
    tf.summary.scalar('accuracy', accuracy)
    merged_summary_op = tf.summary.merge_all()
    # 数据保存器的初始化
    saver = tf.train.Saver()

    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())

        inc_v1.op.run()  # 测试参数传递
        train_path = os.path.join(tmp_path, "train")
        test_path = os.path.join(tmp_path, "test")

        train_writer = tf.summary.FileWriter(train_path + TIMESTAMP, graph=tf.get_default_graph())
        test_writer = tf.summary.FileWriter(test_path + TIMESTAMP, graph=tf.get_default_graph())
        tag = 1
        for n in range(5000):
            for i in range(num_batch):
                batch_x = train_x[i * batch_size: (i + 1) * batch_size]
                batch_y = train_y[i * batch_size: (i + 1) * batch_size]
                # 开始训练数据，同时训练三个变量，返回三个数据
                _, loss, train_result = sess.run([train_step, cross_entropy, merged_summary_op],
                                                 feed_dict={x: batch_x, y_: batch_y, keep_prob_5: 0.5,
                                                            keep_prob_75: 0.75})
                train_writer.add_summary(train_result, n * num_batch + i)
                # 打印损失
                print(n * num_batch + i, "loss", loss)

                # if (n*num_batch+i) % 100 == 0:
                #     # 获取测试数据的准确率
                #     acc = accuracy.eval({x:test_x, y_:test_y, keep_prob_5:1.0, keep_prob_75:1.0})
                #     print(n*num_batch+i,"accuracy", acc)
                #     # 准确率大于0.98时保存并退出
                #     if acc > 0.98 and n > 2:
                #         saver.save(sess, './train_faces.model', global_step=n*num_batch+i)
                #         sys.exit(0)

                # n1 = n
                # num_batch1 = num_batch
                # i1 = i
                acc, test_result = sess.run([accuracy, merged_summary_op],
                                            feed_dict={x: test_x, y_: test_y, keep_prob_5: 1.0, keep_prob_75: 1.0})
                # acc = accuracy.eval({x: test_x, y_: test_y, keep_prob_5: 1.0, keep_prob_75: 1.0})
                test_writer.add_summary(test_result, n * num_batch + i)
                # saver.save(sess, './train_faces.model', global_step=n1 * num_batch1 + i1)
                print(n * num_batch + i, 'accuracy', acc)
                if acc > 0.99:
                    saver.save(sess, tmp_path + '/model.ckpt')
                    # sys.exit(0)
                    tag = 0
                    break;
            if tag == 0:
                break

        saver.save(sess, tmp_path + '/model.ckpt')


@is_admin_login
def anti_proof_train(request):
    if request.method == 'POST':

        # uname = "tensorboard"
        # uname_arg = "--logdir=/root/zlf_projects/pycharm_project_48/static/anti_proof_dataset/tmp/"
        # print("Gathering system information with %s command:\n" % uname)

        # try:
        #     ssh = paramiko.SSHClient()
        #     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #     ssh.connect('39.98.169.35', 22, 'root', 'QWqw12!@')
        #     # tensorboard --logdir=/root/zlf_projects/pycharm_project_48/static/anti_proof_dataset/tmp/
        #     # ssh.exec_command(
        #     #     'tensorboard --logdir=/root/zlf_projects/pycharm_project_48/static/anti_proof_dataset/tmp/ --port 6006')
        #     ssh.exec_command("python3 ./zlf_projects/pycharm_project_48/manage.py runserver 0.0.0.0:8001")
        #     print("check status OK\n")
        #     # ssh.close()
        # except Exception as ex:
        #     print("\tError %s\n" % ex)

        # subprocess.call([uname, uname_arg])

        TIMESTAMP = "{0:%Y-%m-%dT%H-%M-%S/}".format(datetime.now())
        imgs = []
        labs = []
        size = 64
        faces_number = 2
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_path = os.path.join(BASE_DIR, "static")
        media_path2 = os.path.join(media_path, "anti_proof_dataset")
        media_path3 = os.path.join(media_path2, "dataset_processed")
        true_path = os.path.join(media_path3, "ClientFace")
        fake_path = os.path.join(media_path3, "ImposterFace")
        for file_dir_name in os.listdir(true_path):
            next_files = true_path + '/' + file_dir_name  # 左斜杠linux与windows都兼容
            for filename in os.listdir(next_files):
                if filename.endswith('.bmp') or filename.endswith('.BMP') or filename.endswith(
                        '.PNG') or filename.endswith('.png') or filename.endswith('.JPG') or filename.endswith('.jpg'):
                    # 三种图像格式,bmp/png/jpg
                    filename = next_files + '/' + filename

                    img = cv2.imread(filename)

                    imgs.append(img)
                    labs.append(true_path)
        for file_dir_name in os.listdir(fake_path):
            next_files = fake_path + '/' + file_dir_name  # 左斜杠linux与windows都兼容
            for filename in os.listdir(next_files):
                if filename.endswith('.bmp') or filename.endswith('.BMP') or filename.endswith(
                        '.PNG') or filename.endswith('.png') or filename.endswith('.JPG') or filename.endswith('.jpg'):
                    # 三种图像格式,bmp/png/jpg
                    filename = next_files + '/' + filename

                    img = cv2.imread(filename)

                    imgs.append(img)
                    labs.append(fake_path)
        imgs = np.array(imgs)
        labs = np.array([[0, 1] if lab == true_path else [1, 0] for lab in labs])

        # 随机划分测试集与训练集
        train_x, test_x, train_y, test_y = train_test_split(imgs, labs, test_size=0.05,
                                                            random_state=random.randint(0, 100))
        # 参数：图片数据的总数，图片的高、宽、通道
        train_x = train_x.reshape(train_x.shape[0], size, size, 3)
        test_x = test_x.reshape(test_x.shape[0], size, size, 3)
        # 将数据转换成小于1的数
        train_x = train_x.astype('float32') / 255.0
        test_x = test_x.astype('float32') / 255.0

        print('train size:%s, test size:%s' % (len(train_x), len(test_x)))
        # 图片块，每次取100张图片
        batch_size = 100
        num_batch = len(train_x) // batch_size

        x = tf.placeholder(tf.float32, [None, size, size, 3])
        y_ = tf.placeholder(tf.float32, [None, faces_number])
        # 这里也是根据识别人脸个数
        keep_prob_5 = tf.placeholder(tf.float32)
        keep_prob_75 = tf.placeholder(tf.float32)

        v1 = tf.get_variable("v1", shape=[3], initializer=tf.zeros_initializer)  # 测试参数传递
        inc_v1 = v1.assign(v1 + 1)
        cnnTrain(num_batch, x, y_, keep_prob_5, keep_prob_75, inc_v1, TIMESTAMP, train_x, test_x, train_y, test_y,
                 batch_size, faces_number)
        # ssh.close()
        return render(request, "operation.html", {"success": "照片防伪神经训练成功"})
    else:
        return redirect("/operation/")


def anti_proof_cnnLayer(x, keep_prob_5, keep_prob_75, W1, b1, W2, b2, W3, b3, Wf, bf, Wout, bout):
    # 第一层
    # W1 = weightVariable([3, 3, 3, 32])  # 卷积核大小(3,3)， 输入通道(3)， 输出通道(32)
    # b1 = biasVariable([32])
    # W1 = tf.get_variable("W1", shape=[3, 3, 3, 32])
    # b1 = tf.get_variable("b1", shape=[32])
    # 卷积
    conv1 = tf.nn.relu(conv2d(x, W1) + b1)
    # 池化
    pool1 = maxPool(conv1)
    # 减少过拟合，随机让某些权重不更新
    drop1 = dropout(pool1, keep_prob_5)

    # 第二层
    # W2 = weightVariable([3, 3, 32, 64])
    # b2 = biasVariable([64])
    # W2 = tf.get_variable("W2", shape=[3, 3, 32, 64])
    # b2 = tf.get_variable("b2", shape=[64])
    conv2 = tf.nn.relu(conv2d(drop1, W2) + b2)
    pool2 = maxPool(conv2)
    drop2 = dropout(pool2, keep_prob_5)

    # 第三层
    # W3 = weightVariable([3, 3, 64, 64])
    # b3 = biasVariable([64])
    # W3 = tf.get_variable("W3", shape=[3, 3, 64, 64])
    # b3 = tf.get_variable("b3", shape=[64])
    conv3 = tf.nn.relu(conv2d(drop2, W3) + b3)
    pool3 = maxPool(conv3)
    drop3 = dropout(pool3, keep_prob_5)

    # 全连接层
    # Wf = weightVariable([8 * 16 * 32, 512])
    # bf = biasVariable([512])
    # Wf = tf.get_variable("Wf", shape=[8 * 8 * 64, 512])
    # bf = tf.get_variable("bf", shape=[512])
    drop3_flat = tf.reshape(drop3, [-1, 8 * 16 * 32])  # 变成8 * 16 * 32列，-1代表行数不知道
    dense = tf.nn.relu(tf.matmul(drop3_flat, Wf) + bf)
    dropf = dropout(dense, keep_prob_75)

    # 输出层
    # Wout = weightVariable([512, 2])
    # bout = biasVariable([2])
    # Wout = tf.get_variable("Wout", shape=[512, 2])
    # bout = tf.get_variable("bout", shape=[2])
    out = tf.add(tf.matmul(dropf, Wout), bout)
    return out


def is_true_face(image, sess, predict, x, keep_prob_5, keep_prob_75):
    res = sess.run(predict, feed_dict={x: [image / 255.0], keep_prob_5: 1.0, keep_prob_75: 1.0})
    print("res", res)
    return res[0]  # 0假1真


def change_img2face(stu_img):
    print("=" * 50)
    print("stu_img", stu_img)
    # 为什么
    print("=" * 50)
    size = 64
    detector = dlib.get_frontal_face_detector()
    img = cv2.imread(stu_img)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dets = detector(gray_image, 1)
    # 此处为了防止dlib检测不到人脸而报错
    face = cv2.resize(img, (size, size))
    for i, d in enumerate(dets):
        x1 = d.top() if d.top() > 0 else 0
        y1 = d.bottom() if d.bottom() > 0 else 0
        x2 = d.left() if d.left() > 0 else 0
        y2 = d.right() if d.right() > 0 else 0
        face = img[x1:y1, x2:y2]
        # print(x1,y1,x2,y2)
        # 调整图片的尺寸
        face = cv2.resize(face, (size, size))
    return face


@is_teacher_login
def students_anti_proof(request):
    if request.method == 'POST':
        attendance_id = request.POST.get("attendance_id")
        atten_info = attendance.objects.filter(att=attendance_id)
        size = 64
        v1 = tf.get_variable("v1", shape=[3])
        W1 = tf.get_variable("W1", shape=[3, 3, 3, 32])
        b1 = tf.get_variable("b1", shape=[32])
        W2 = tf.get_variable("W2", shape=[3, 3, 32, 64])
        b2 = tf.get_variable("b2", shape=[64])
        W3 = tf.get_variable("W3", shape=[3, 3, 64, 64])
        b3 = tf.get_variable("b3", shape=[64])
        Wf = tf.get_variable("Wf", shape=[8 * 8 * 64, 512])
        bf = tf.get_variable("bf", shape=[512])
        Wout = tf.get_variable("Wout", shape=[512, 2])
        bout = tf.get_variable("bout", shape=[2])
        for row in atten_info:
            stu_img1 = row.img1
            stu_img2 = row.img2
            stu_img3 = row.img3
            print(stu_img1)
            print(stu_img2)
            print(stu_img3)

            x = tf.placeholder(tf.float32, [None, size, size, 3])
            y_ = tf.placeholder(tf.float32, [None, 2])

            keep_prob_5 = tf.placeholder(tf.float32)  # dropout
            keep_prob_75 = tf.placeholder(tf.float32)

            # v1 = tf.get_variable("v1", shape=[3])

            output = anti_proof_cnnLayer(x, keep_prob_5, keep_prob_75, W1, b1, W2, b2, W3, b3, Wf, bf, Wout, bout)
            predict = tf.argmax(output, 1)  # 将output中向量行找最大索引

            saver = tf.train.Saver()  # 将训练后的变量保存

            # print('Is this my face? %s' % is_true_face(face))
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            media_path = os.path.join(BASE_DIR, "static")
            media_path2 = os.path.join(media_path, "anti_proof_dataset")
            tmp_path = os.path.join(media_path2, "tmp")
            print("+" * 50)
            face = change_img2face(stu_img1)
            print("+" * 50)
            with tf.Session() as sess:
                saver.restore(sess, tmp_path + "/model.ckpt")
                print("v1 : %s" % v1.eval())
                anti_proof_tag = is_true_face(face, sess, predict, x, keep_prob_5, keep_prob_75)
                print('is true face?', anti_proof_tag)
                if (anti_proof_tag == 0):
                    # print("假人")
                    face = change_img2face(stu_img2)
                    anti_proof_tag = is_true_face(face, sess, predict, x, keep_prob_5, keep_prob_75)
                    if (anti_proof_tag == 0):
                        face = change_img2face(stu_img3)
                        anti_proof_tag = is_true_face(face, sess, predict, x, keep_prob_5, keep_prob_75)
                        if (anti_proof_tag == 0):
                            print("假人")
                            attendance.objects.filter(stu=row.stu, att=row.att).update(
                                complain_tag=str(int(row.complain_tag) + 1))
                        else:
                            print("真人")
                            attendance.objects.filter(stu=row.stu, att=row.att).update(tag=str(int(row.tag) + 3),
                                                                                       complain_tag=str(
                                                                                           int(row.complain_tag) + 1))
                    else:
                        print("真人")
                        attendance.objects.filter(stu=row.stu, att=row.att).update(tag=str(int(row.tag) + 3),
                                                                                   complain_tag=str(
                                                                                       int(row.complain_tag) + 1))

                # elif (anti_proof_tag == 1):
                #     print("真人")
                else:
                    # print("模式错误")
                    print("真人")
                    attendance.objects.filter(stu=row.stu, att=row.att).update(tag=str(int(row.tag) + 3),
                                                                               complain_tag=str(
                                                                                   int(row.complain_tag) + 1))
                    # print('is true face? %s' % anti_proof_tag)
                # num = input("number:")
                # my_face = cv2.imread("C:/Users/46507/PycharmProjects/LearnTF/my_faces/" + num + ".bmp")
                # # 换目录使用../other_faces/1
                # print('my face? %s' % is_true_face(my_face))
                #
                # cv2.rectangle(img, (x2, x1), (y2, y1), (255, 0, 0), 3)
                # cv2.imshow('face', face)
        # 这里只能假设都为真
        return HttpResponse("活体检测成功")
    else:
        return redirect("/teacher_manage_atten/")


# 读取文件内的所有,迭代，将生成的图片与原图片放在同一文件夹下

def read_file_all(data_dir_path):
    for f in os.listdir(data_dir_path):
        print("data_dir_path:", data_dir_path)
        data_file_path = os.path.join(data_dir_path, f)
        if os.path.isfile(data_file_path):
            image_rotate(data_file_path, data_dir_path)

            # print(collected)
        else:
            read_file_all(data_file_path)
            # 文件夹下套文件夹情况


def read_file_all_again(data_dir_path):
    for f in os.listdir(data_dir_path):
        print("data_dir_path:", data_dir_path)
        data_file_path = os.path.join(data_dir_path, f)
        if os.path.isfile(data_file_path):
            relight(data_file_path, data_dir_path, random.uniform(0.5, 1.5), random.randint(-50, 50))
        else:
            read_file_all_again(data_file_path)
    # 文件夹下套文件夹情况


# 改变图片的亮度与对比度
def relight(image_path, save_dir, light=1, bias=0):
    img = Image.open(image_path)
    img = np.array(img)
    w = img.shape[1]
    h = img.shape[0]
    # image = []
    for i in range(w):
        for j in range(h):
            for c in range(3):  # 三通道
                tmp = int(img[j, i, c] * light + bias)
                if tmp > 255:
                    tmp = 255
                elif tmp < 0:
                    tmp = 0
                img[j, i, c] = tmp
    img = Image.fromarray(img)
    save_path = save_dir + "/" + random_name() + '.bmp'
    img.save(save_path)
    print("save_path:", save_path)


def image_rotate(image_path, save_dir):
    # 读取图像
    im = Image.open(image_path)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)  # 左右互换
    save_path = save_dir + "/" + random_name() + '.bmp'
    im.save(save_path)
    print("save_path:", save_path)


# img=np.array(Image.open(image_path))
# #随机生成100个椒盐
# rows,cols,dims=img.shape
# for i in range(100):
# x=np.random.randint(0,rows)
# y=np.random.randint(0,cols)
# img[x,y,:]=255
# img.flags.writeable = True  # 将数组改为读写模式
# dst=Image.fromarray(np.uint8(img))
# save_path = save_dir + "/" + random_name() + '.bmp'
# dst.save(save_path)
# print("save_path:",save_path)
def random_name():
    # 随机数，用来随机取名字
    a_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    name = random.sample(a_list, 5)
    file_name = "".join(name)
    return file_name


def readData(path, imgs, labs):
    dict_match = {}
    num = 0
    for file_dir_name in os.listdir(path):
        next_files = path + '/' + file_dir_name  # 左斜杠linux与windows都兼容

        dict_match.setdefault(num, "0")
        print("dict_match", dict_match)
        dict_match[num] = file_dir_name
        print("dict_match", dict_match)

        for filename in os.listdir(next_files):
            if filename.endswith('.bmp') or filename.endswith('.BMP') or filename.endswith('.PNG') or filename.endswith(
                    '.png') or filename.endswith('.JPG') or filename.endswith('.jpg'):
                # 三种图像格式,bmp/png/jpg
                filename = path + '/' + file_dir_name + '/' + filename

                img = cv2.imread(filename)

                imgs.append(img)
                # labs.append(file_dir_name)
                labs.append(num)
        num += 1
    sorted_x = sorted(dict_match.items(), key=operator.itemgetter(0))

    dict_match_json = {
        'version': "1.0",
        'results': sorted_x,
        'explain': {
            'used': True,
            'details': "this is for dict_match josn when you train",
        }
    }
    json_str = json.dumps(dict_match_json, indent=4)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media_path = os.path.join(BASE_DIR, "static")
    tmp_dir = os.path.join(media_path, "tmp")
    json_path = tmp_dir + '/dict_match.json'
    with open(json_path, 'w') as json_file:
        json_file.write(json_str)
    return imgs, labs


# face_recognition_start
def face_recognition_weightVariable(shape):
    init = tf.random_normal(shape, stddev=0.01)
    return tf.Variable(init)


def face_recognition_biasVariable(shape):
    init = tf.random_normal(shape)
    return tf.Variable(init)


def face_recognition_conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def face_recognition_maxPool(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def face_recognition_dropout(x, keep):
    return tf.nn.dropout(x, keep)


def face_recognition_cnnLayer(x, faces_number, keep_prob_5, keep_prob_75):
    # 第一层
    # W1 = weightVariable([3,3,3,32]) # 卷积核大小(3,3)， 输入通道(3)， 输出通道(32)
    W1 = tf.get_variable("W1", shape=[3, 3, 3, 32], initializer=tf.random_normal_initializer(stddev=0.01))
    # b1 = biasVariable([32])
    b1 = tf.get_variable("b1", shape=[32], initializer=tf.random_normal_initializer)
    # 卷积
    conv1 = tf.nn.relu(face_recognition_conv2d(x, W1) + b1)
    # 池化
    pool1 = face_recognition_maxPool(conv1)
    # 减少过拟合，随机让某些权重不更新
    drop1 = face_recognition_dropout(pool1, keep_prob_5)

    # 第二层
    # W2 = weightVariable([3,3,32,64])
    W2 = tf.get_variable("W2", shape=[3, 3, 32, 64], initializer=tf.random_normal_initializer(stddev=0.01))
    # b2 = biasVariable([64])
    b2 = tf.get_variable("b2", shape=[64], initializer=tf.random_normal_initializer)
    conv2 = tf.nn.relu(face_recognition_conv2d(drop1, W2) + b2)
    pool2 = face_recognition_maxPool(conv2)
    drop2 = face_recognition_dropout(pool2, keep_prob_5)

    # 第三层
    # W3 = weightVariable([3,3,64,64])
    W3 = tf.get_variable("W3", shape=[3, 3, 64, 64], initializer=tf.random_normal_initializer(stddev=0.01))
    # b3 = biasVariable([64])
    b3 = tf.get_variable("b3", shape=[64], initializer=tf.random_normal_initializer)
    conv3 = tf.nn.relu(face_recognition_conv2d(drop2, W3) + b3)
    pool3 = face_recognition_maxPool(conv3)
    drop3 = face_recognition_dropout(pool3, keep_prob_5)

    # 全连接层
    # Wf = weightVariable([8*8*64, 512])
    Wf = tf.get_variable("Wf", shape=[8 * 8 * 64, 512], initializer=tf.random_normal_initializer(stddev=0.01))
    # bf = biasVariable([512])
    bf = tf.get_variable("bf", shape=[512], initializer=tf.random_normal_initializer)
    drop3_flat = tf.reshape(drop3, [-1, 8 * 8 * 64])
    dense = tf.nn.relu(tf.matmul(drop3_flat, Wf) + bf)
    dropf = face_recognition_dropout(dense, keep_prob_75)

    # 输出层
    # Wout = weightVariable([512, 2])
    Wout = tf.get_variable("Wout", shape=[512, faces_number], initializer=tf.random_normal_initializer(stddev=0.01))
    # bout = biasVariable([2])
    bout = tf.get_variable("bout", shape=[faces_number], initializer=tf.random_normal_initializer)
    # out = tf.matmul(dropf, Wout) + bout
    out = tf.add(tf.matmul(dropf, Wout), bout)
    return out


# 输出层个数根据标签决定
def face_recognition_cnnTrain(train_x, train_y, test_x, test_y, TIMESTAMP, num_batch, x, y_, keep_prob_5, keep_prob_75,
                              inc_v1,
                              batch_size, faces_number):
    tag = 0  # 结束标志
    out = face_recognition_cnnLayer(x, faces_number, keep_prob_5, keep_prob_75)

    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=out, labels=y_))
    # learning rate = 0.01
    train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)
    # 比较标签是否相等，再求的所有数的平均值，tf.cast(强制转换类型)
    # accuracy = tf.reduce_mean(tf.cast(tf.equal(out, y_), tf.float32))
    accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(out, 1), tf.argmax(y_, 1)), tf.float32))
    # 将loss与accuracy保存以供tensorboard使用
    tf.summary.scalar('loss', cross_entropy)
    tf.summary.scalar('accuracy', accuracy)
    merged_summary_op = tf.summary.merge_all()
    # 数据保存器的初始化
    saver = tf.train.Saver()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media_path = os.path.join(BASE_DIR, "static")
    tmp_dir = os.path.join(media_path, "tmp")
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    train_dir = os.path.join(tmp_dir, "train")
    test_dir = os.path.join(tmp_dir, "test")

    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())

        inc_v1.op.run()  # 测试参数传递

        train_writer = tf.summary.FileWriter(train_dir + TIMESTAMP, graph=tf.get_default_graph())
        test_writer = tf.summary.FileWriter(test_dir + TIMESTAMP, graph=tf.get_default_graph())

        for n in range(5000):
            for i in range(num_batch):
                batch_x = train_x[i * batch_size: (i + 1) * batch_size]
                batch_y = train_y[i * batch_size: (i + 1) * batch_size]
                # 开始训练数据，同时训练三个变量，返回三个数据
                _, loss, train_result = sess.run([train_step, cross_entropy, merged_summary_op],
                                                 feed_dict={x: batch_x, y_: batch_y, keep_prob_5: 0.5,
                                                            keep_prob_75: 0.75})
                train_writer.add_summary(train_result, n * num_batch + i)
                # 打印损失
                print(n * num_batch + i, "loss", loss)

                # if (n*num_batch+i) % 100 == 0:
                #     # 获取测试数据的准确率
                #     acc = accuracy.eval({x:test_x, y_:test_y, keep_prob_5:1.0, keep_prob_75:1.0})
                #     print(n*num_batch+i,"accuracy", acc)
                #     # 准确率大于0.98时保存并退出
                #     if acc > 0.98 and n > 2:
                #         saver.save(sess, './train_faces.model', global_step=n*num_batch+i)
                #         sys.exit(0)

                # n1 = n
                # num_batch1 = num_batch
                # i1 = i
                acc, test_result = sess.run([accuracy, merged_summary_op],
                                            feed_dict={x: test_x, y_: test_y, keep_prob_5: 1.0, keep_prob_75: 1.0})
                # acc = accuracy.eval({x: test_x, y_: test_y, keep_prob_5: 1.0, keep_prob_75: 1.0})
                test_writer.add_summary(test_result, n * num_batch + i)
                # saver.save(sess, './train_faces.model', global_step=n1 * num_batch1 + i1)
                print(n * num_batch + i, 'accuracy', acc)
                # if acc > 0.94:
                if acc > 0.76:
                    saver.save(sess, tmp_dir + '/model.ckpt')
                    # sys.exit(0)
                    tag = 1
                    break
            if (tag == 1):
                break

        saver.save(sess, tmp_dir + '/model.ckpt')


# face_recognition_end

@is_teacher_login
def train(request):
    if request.method == 'POST':
        courseNum = request.POST.get("courseNum")
        email = request.COOKIES["qwer"]
        teacher_model = TeacherInfo.objects.get(email=email)
        course_model = CourseInfo.objects.get(courseNum=courseNum)
        choose_course_model = choose_course.objects.filter(cour=course_model, teac=teacher_model)

        # 图片预处理，裁剪
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_path = os.path.join(BASE_DIR, "static")
        input_dir = os.path.join(media_path, "train_set")
        output_dir = os.path.join(media_path, "processed_train_set")

        if os.path.exists(output_dir):
            output_dir_list = os.listdir(output_dir)
            for file in output_dir_list:
                file_next_path = os.path.join(output_dir, file)
                file_next_path_list = os.listdir(file_next_path)
                for file_next in file_next_path_list:
                    file_final = os.path.join(file_next_path, file_next)
                    print("file_final", file_final)
                    os.remove(file_final)
                os.removedirs(file_next_path)
            # os.removedirs(output_dir)  # 里面文件夹都为空时才能删除成功
        os.mkdir(output_dir)
        size = 64
        # 使用dlib自带的frontal_face_detector作为我们的特征提取器
        detector = dlib.get_frontal_face_detector()

        dirnames = os.listdir(input_dir)
        # print(dirnames)
        # for (path, dirnames, filenames) in os.walk(input_dir):
        #     print("path", path)
        #     print("dirnames", dirnames)
        for dir in dirnames:

            new_path = output_dir + "/" + dir
            isExists = os.path.exists(new_path)
            # 判断结果
            if not isExists:
                # 如果不存在则创建目录
                # 创建目录操作函数
                os.makedirs(new_path)

                print(new_path + ' 创建成功')
            else:
                # 如果目录存在则不创建，并提示目录已存在
                print(new_path + ' 目录已存在')
                continue

            next_dir = input_dir + "/" + dir
            for (next_path, next_dirnames, next_filenames) in os.walk(next_dir):
                print("next_filenames", next_filenames)
                for filename in next_filenames:
                    if filename.endswith('.bmp') or filename.endswith('.BMP') or filename.endswith(
                            '.PNG') or filename.endswith('.png') or filename.endswith('.JPG') or filename.endswith(
                        '.jpg'):
                        picture_name = os.path.basename(filename)  # 获取当前文件名
                        print('Being processed picture %s' % picture_name)
                        img_path = next_path + '/' + filename
                        # 从文件读取图片
                        img = cv2.imread(img_path)
                        # 转为灰度图片
                        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        # 使用detector进行人脸检测 dets为返回的结果
                        dets = detector(gray_img, 1)

                        # 使用enumerate 函数遍历序列中的元素以及它们的下标
                        # 下标i即为人脸序号
                        # left：人脸左边距离图片左边界的距离 ；right：人脸右边距离图片左边界的距离
                        # top：人脸上边距离图片上边界的距离 ；bottom：人脸下边距离图片上边界的距离
                        for i, d in enumerate(dets):
                            x1 = d.top() if d.top() > 0 else 0
                            y1 = d.bottom() if d.bottom() > 0 else 0
                            x2 = d.left() if d.left() > 0 else 0
                            y2 = d.right() if d.right() > 0 else 0
                            # img[y:y+h,x:x+w]
                            face = img[x1:y1, x2:y2]
                            # 调整图片的尺寸
                            face = cv2.resize(face, (size, size))
                            # cv2.imshow('image', face)
                            # 保存图片
                            cv2.imwrite(new_path + '/' + picture_name, face)
                    # key = cv2.waitKey(30) & 0xff
                    # if key == 27:
                    # sys.exit(0)
        print("[INFO]end of processing - cut images")

        # 图片预处理，扩数据集
        data_dir_path = output_dir  # 读取/保存的文件路径
        read_file_all(data_dir_path)
        read_file_all_again(data_dir_path)

        print("[INFO]end of processing - enlarge images")

        # 开始训练
        TIMESTAMP = "{0:%Y-%m-%dT%H-%M-%S/}".format(datetime.now())

        # my_faces_path = './my_faces'
        # # other_faces_path = './other_faces'
        face_path = output_dir  # 数据集路径
        size = 64

        imgs = []
        labs = []

        # readData(my_faces_path)
        # readData(other_faces_path)
        imgs, labs = readData(face_path, imgs, labs)

        # 将图片数据与标签转换成数组
        imgs = np.array(imgs)
        # labs = np.array([[0, 1] if lab == my_faces_path else [1, 0] for lab in labs])
        labs_mid = labs
        labs_set = labs
        image_numbers = len(labs)
        faces_number = len(set(labs_set))
        labs = np.zeros((image_numbers, faces_number), dtype=np.int)
        labs_index = 0
        for x in labs_mid:
            labs[labs_index][int(x)] = 1
            labs_index = labs_index + 1
        # 随机划分测试集与训练集
        train_x, test_x, train_y, test_y = train_test_split(imgs, labs, test_size=0.05,
                                                            random_state=random.randint(0, 100))
        # 参数：图片数据的总数，图片的高、宽、通道
        train_x = train_x.reshape(train_x.shape[0], size, size, 3)
        test_x = test_x.reshape(test_x.shape[0], size, size, 3)
        # 将数据转换成小于1的数
        train_x = train_x.astype('float32') / 255.0
        test_x = test_x.astype('float32') / 255.0

        print('train size:%s, test size:%s' % (len(train_x), len(test_x)))
        # 图片块，每次取100张图片
        batch_size = 100
        num_batch = len(train_x) // batch_size

        x = tf.placeholder(tf.float32, [None, size, size, 3])
        y_ = tf.placeholder(tf.float32, [None, faces_number])
        # 这里也是根据识别人脸个数
        keep_prob_5 = tf.placeholder(tf.float32)
        keep_prob_75 = tf.placeholder(tf.float32)

        v1 = tf.get_variable("v1", shape=[3], initializer=tf.zeros_initializer)  # 测试参数传递
        inc_v1 = v1.assign(v1 + 1)

        face_recognition_cnnTrain(train_x, train_y, test_x, test_y, TIMESTAMP, num_batch, x, y_, keep_prob_5,
                                  keep_prob_75, inc_v1,
                                  batch_size,
                                  faces_number)
        # for row in choose_course_model:
        #     # row.stu

        return HttpResponse("训练成功")
    else:
        return redirect("/create_course/")


def getPaddingSize(img):
    h, w, _ = img.shape
    top, bottom, left, right = (0, 0, 0, 0)
    longest = max(h, w)

    if w < longest:
        tmp = longest - w
        # //表示整除符号
        left = tmp // 2
        right = tmp - left
    elif h < longest:
        tmp = longest - h
        top = tmp // 2
        bottom = tmp - top
    else:
        pass
    return top, bottom, left, right


def student_recognition_cnnLayer(x, W1, b1, keep_prob_5, W2, b2, W3, b3, keep_prob_75, Wf, bf, Wout, bout):
    # 第一层
    # W1 = weightVariable([3, 3, 3, 32])  # 卷积核大小(3,3)， 输入通道(3)， 输出通道(32)
    # b1 = biasVariable([32])

    # 卷积
    conv1 = tf.nn.relu(conv2d(x, W1) + b1)
    # 池化
    pool1 = maxPool(conv1)
    # 减少过拟合，随机让某些权重不更新
    drop1 = dropout(pool1, keep_prob_5)

    # 第二层
    # W2 = weightVariable([3, 3, 32, 64])
    # b2 = biasVariable([64])

    conv2 = tf.nn.relu(conv2d(drop1, W2) + b2)
    pool2 = maxPool(conv2)
    drop2 = dropout(pool2, keep_prob_5)

    # 第三层
    # W3 = weightVariable([3, 3, 64, 64])
    # b3 = biasVariable([64])

    conv3 = tf.nn.relu(conv2d(drop2, W3) + b3)
    pool3 = maxPool(conv3)
    drop3 = dropout(pool3, keep_prob_5)

    # 全连接层
    # Wf = weightVariable([8 * 16 * 32, 512])
    # bf = biasVariable([512])

    drop3_flat = tf.reshape(drop3, [-1, 8 * 16 * 32])  # 变成8 * 16 * 32列，-1代表行数不知道
    dense = tf.nn.relu(tf.matmul(drop3_flat, Wf) + bf)
    dropf = dropout(dense, keep_prob_75)

    # 输出层
    # Wout = weightVariable([512, 2])
    # bout = biasVariable([2])

    out = tf.add(tf.matmul(dropf, Wout), bout)
    return out


def whose_face(image, sess, predict, x, keep_prob_5, keep_prob_75):
    res = sess.run(predict, feed_dict={x: [image / 255.0], keep_prob_5: 1.0, keep_prob_75: 1.0})
    print("res", res)
    return res[0]


# MY_DBSCAN : a custom DBSCAN algorithm implementation for 1D values only
class DBSCAN_1D:

    # 1D distance
    def distance_1D(self, num1, num2):
        return abs(num1 - num2)

    def regionQuery(self, P):
        neighbourPts = []
        for point in self.D:
            if point not in self.visited:
                if self.distance_1D(P, point) < self.eps:
                    neighbourPts.append(point)

        return neighbourPts

    def inAnyCluster(self, point):
        for cluster in self.C:
            if point in cluster:
                return True
        return False

    def expandCluster(self, P, neighbourPts):
        # first append the current point to this new cluster
        # self.C[self.c_n].append(P)
        # for each of the points in the neighbourhood

        for point in neighbourPts:
            if point not in self.visited:
                self.visited.append(point)
                neighbourPts_2 = self.regionQuery(point)

                # if len(neighbourPts_2) >= self.MinPts:
                # adds all the neighbours to the list of neighbours
                # this includes previous points already in the list potentially, but we don't care
                # as those will be filtered by the visited list
                neighbourPts += neighbourPts_2
                # adds the point to the cluster if not in any cluster yet
                if not self.inAnyCluster(point):
                    # print("Adding ", point, " to the cluster ", self.C[self.c_n])
                    self.C[self.c_n].append(point)

    def show_clusters(self):
        print("Discarded cluster(s):", len(self.noise))
        count = 0
        for noise_cluster in self.noise:
            count = count + 1
            print("Discarded cluster ", count, " = ", noise_cluster)

        print("No. of clusters: ", len(self.C))
        count = 0
        longest_cluster = []
        longest_cluster_num = 0
        for cluster in self.C:
            count = count + 1
            # print (cluster)
            # print(col)
            print("Cluster ", count, " = ", cluster)
            print(cluster.__len__())
            if (cluster.__len__() > longest_cluster_num):
                longest_cluster_num = cluster.__len__()
                longest_cluster = cluster
        print("==longest_cluster==")
        print(longest_cluster_num)
        print(longest_cluster)
        longest_cluster.sort()
        min_dbm = longest_cluster[0]
        print(longest_cluster[0])  # 班内学生最小信号强度值
        return min_dbm

    def __init__(self, D, eps, MinPts):
        self.D = D
        self.eps = eps
        self.MinPts = MinPts
        self.noise = []
        self.visited = []
        self.C = []
        self.c_n = -1

        # run through all the points in the data
        for point in D:
            self.visited.append(point)  # marking point as visited

            # gets all the neighbouring points within the distance defined by eps
            neighbourPts = self.regionQuery(point)

            if not self.inAnyCluster(point):
                self.C.append([])
                self.c_n += 1
                # print("Adding ", point, " to the cluster ", self.C[self.c_n])
                self.C[self.c_n].append(point)
                # see if we can expand the cluster further by adding points
                # until there is a gap of eps
                self.expandCluster(point, neighbourPts)
            # point was completely expanded and cluster is complete

            # if the length of the cluster is not long enough discard it
            if len(self.C[self.c_n]) < (self.MinPts):
                self.noise.append(self.C[self.c_n])
                del (self.C[self.c_n])
                self.c_n -= 1


@is_teacher_login
def wifi_finger(request):
    if request.method == 'POST':
        attendance_id = request.POST.get("attendance_id")
        atten_info = attendance.objects.filter(att=attendance_id)
        dbm_list = []
        for row in atten_info:
            dbm_list.append(int(row.dbm))
        eps = 4
        MinPts = 1
        my_dbscan = DBSCAN_1D(dbm_list, eps, MinPts)
        min_dbm = my_dbscan.show_clusters()
        for row in atten_info:
            if (int(row.dbm) < min_dbm):
                attendance.objects.filter(stu=row.stu, att=row.att).update(complain_tag=str(int(row.complain_tag) + 1))
            else:
                attendance.objects.filter(stu=row.stu, att=row.att).update(tag=str(int(row.tag) + 2),
                                                                           complain_tag=str(int(row.complain_tag) + 1))

        return HttpResponse("学生考勤成功")
    else:
        return redirect("/teacher_manage_atten/")


@is_teacher_login
def face_recognition_students(request):
    if request.method == 'POST':
        attendance_id = request.POST.get("attendance_id")
        atten_info = attendance.objects.filter(att=attendance_id)

        size = 64

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media_path = os.path.join(BASE_DIR, "static")
        tmp_dir = os.path.join(media_path, "tmp")
        json_path = tmp_dir + '/dict_match.json'

        with open(json_path, 'r') as load_f:
            load_dict = json.load(load_f)

        students_number = len(load_dict["results"])

        match_list = load_dict["results"]

        x = tf.placeholder(tf.float32, [None, size, size, 3])
        y_ = tf.placeholder(tf.float32, [None, students_number])

        keep_prob_5 = tf.placeholder(tf.float32)  # dropout
        keep_prob_75 = tf.placeholder(tf.float32)

        v1 = tf.get_variable("v1", shape=[3])

        W1 = tf.get_variable("W1", shape=[3, 3, 3, 32])
        b1 = tf.get_variable("b1", shape=[32])
        W2 = tf.get_variable("W2", shape=[3, 3, 32, 64])
        b2 = tf.get_variable("b2", shape=[64])
        W3 = tf.get_variable("W3", shape=[3, 3, 64, 64])
        b3 = tf.get_variable("b3", shape=[64])
        Wf = tf.get_variable("Wf", shape=[8 * 8 * 64, 512])
        bf = tf.get_variable("bf", shape=[512])
        Wout = tf.get_variable("Wout", shape=[512, students_number])
        bout = tf.get_variable("bout", shape=[students_number])

        output = student_recognition_cnnLayer(x, W1, b1, keep_prob_5, W2, b2, W3, b3, keep_prob_75, Wf, bf, Wout, bout)
        predict = tf.argmax(output, 1)  # 将output中向量行找最大索引

        saver = tf.train.Saver()  # 将训练后的变量保存

        with tf.Session() as sess:
            for row in atten_info:
                stu_face = change_img2face(row.img1)
                saver.restore(sess, tmp_dir + "/model.ckpt")
                print("v1 : %s" % v1.eval())
                which_one = whose_face(stu_face, sess, predict, x, keep_prob_5, keep_prob_75)
                print('Whose face? %s' % which_one)

                end_tag = 0
                for num_list in match_list:
                    if (num_list[0] == which_one):
                        if (num_list[1] == row.stu.studentNum):
                            attendance.objects.filter(stu=row.stu, att=row.att).update(tag=str(int(row.tag) + 4),
                                                                                       complain_tag=str(
                                                                                           int(row.complain_tag) + 1))
                            print("出勤")
                            end_tag = 1
                        else:
                            stu_face = change_img2face(row.img2)
                            saver.restore(sess, tmp_dir + "/model.ckpt")
                            print("v1 : %s" % v1.eval())
                            which_one = whose_face(stu_face, sess, predict, x, keep_prob_5, keep_prob_75)
                            print('Whose face? %s' % which_one)
                            for num_list in match_list:
                                if (num_list[0] == which_one):
                                    if (num_list[1] == row.stu.studentNum):
                                        attendance.objects.filter(stu=row.stu, att=row.att).update(
                                            tag=str(int(row.tag) + 4), complain_tag=str(int(row.complain_tag) + 1))
                                        print("出勤")
                                        end_tag = 1
                                    else:
                                        stu_face = change_img2face(row.img3)
                                        saver.restore(sess, tmp_dir + "/model.ckpt")
                                        print("v1 : %s" % v1.eval())
                                        which_one = whose_face(stu_face, sess, predict, x, keep_prob_5, keep_prob_75)
                                        print('Whose face? %s' % which_one)
                                        for num_list in match_list:
                                            if (num_list[0] == which_one):
                                                if (num_list[1] == row.stu.studentNum):
                                                    attendance.objects.filter(stu=row.stu, att=row.att).update(
                                                        tag=str(int(row.tag) + 4),
                                                        complain_tag=str(int(row.complain_tag) + 1))
                                                    print("出勤")
                                                    end_tag = 1
                                                else:
                                                    attendance.objects.filter(stu=row.stu, att=row.att).update(
                                                        complain_tag=str(int(row.complain_tag) + 1))
                                                    print("缺勤")
                                                    end_tag = 1
                                            else:
                                                continue

                                            if (end_tag == 1):
                                                break
                                else:
                                    continue
                                if (end_tag == 1):
                                    break

                    else:
                        continue
                    if (end_tag == 1):
                        break

        return HttpResponse("学生考勤成功")
    else:
        return redirect("/teacher_manage_atten/")


@is_admin_login
def manage_student_account(request):
    if request.method == 'POST':
        student_code = request.POST.get('student_code')
        UserInfo.objects.filter(studentNum=student_code).delete()
    else:
        pass
    students = UserInfo.objects.filter()
    return render(request, "manage_student_account.html", {"students": students})


@is_admin_login
def manage_teacher_account(request):
    if request.method == 'POST':
        teacher_code = request.POST.get('teacher_code')
        TeacherInfo.objects.filter(teacherNum=teacher_code).delete()
    else:
        pass
    teachers = TeacherInfo.objects.filter()
    return render(request, "manage_teacher_account.html", {"teachers": teachers})


@is_teacher_login
def delete_attendance(request):
    if request.method == 'POST':
        attendance_id = request.POST.get('attendance_id')
        course_id = AttendanceInfo.objects.filter(attendance_id=attendance_id)[0].course_id.courseNum
        AttendanceInfo.objects.filter(attendance_id=attendance_id).delete()
        email = request.COOKIES["qwer"]
        teacher_model = TeacherInfo.objects.get(email=email)
        teacherNum = teacher_model.teacherNum
        atten_infos = AttendanceInfo.objects.filter(teacher_id=teacherNum, course_id=course_id)
        return render(request, "teacher_atten_course.html", {"atten_infos": atten_infos})
    else:
        return redirect("/teacher_manage_atten/")


@is_teacher_login
def delete_course(request):
    if request.method == 'POST':
        email = request.COOKIES["qwer"]
        teacher_model = TeacherInfo.objects.get(email=email)
        teacherNum = teacher_model.teacherNum
        courseNum = request.POST.get('courseNum')
        # print(Teacher2Course.objects.filter(course_id=courseNum).count())
        Teacher2Course.objects.filter(course_id=courseNum, teacher_id=teacherNum).delete()
        # print(Teacher2Course.objects.filter(course_id=courseNum).count())
        if (Teacher2Course.objects.filter(course_id=courseNum).count() == 0):
            CourseInfo.objects.filter(courseNum=courseNum).delete()
    return redirect("/create_course/")


@is_teacher_login
def delete_choose_course(request):
    if request.method == 'POST':
        email = request.COOKIES["qwer"]
        teacher_model = TeacherInfo.objects.get(email=email)
        teacherNum = teacher_model.teacherNum
        courseNum = request.POST.get('cour_id')
        studentNum = request.POST.get('stu_id')
        choose_course.objects.filter(stu=studentNum, teac=teacherNum, cour=courseNum).delete()
        results = choose_course.objects.filter(cour=courseNum, teac=teacherNum)
        return render(request, "watch_students.html", {"results": results, "courseNum": courseNum})
    else:
        return redirect("/create_course/")


@is_login
def stu_check_atten(request):
    if request.method == 'POST':
        email = request.COOKIES["qwer"]
        student_model = UserInfo.objects.get(email=email)
        course_id = request.POST.get("cour_id")
        teacher_id = request.POST.get("teac_id")
        stu_atten_results = []
        atten_info_results = AttendanceInfo.objects.filter(course_id=course_id, teacher_id=teacher_id)
        for row in atten_info_results:
            stu_atten_results.append(attendance.objects.filter(stu=student_model, att=row.attendance_id)[0])
        return render(request, "stu_check_atten.html",
                      {"stu_atten_results": stu_atten_results})
    else:
        return redirect("/chosen_course/")


@is_login
def attendance_complain(request):
    if request.method == 'POST':
        attendance_id = request.POST.get("attendance_id")
        att = AttendanceInfo.objects.filter(attendance_id=attendance_id)[0]
        # print(att.course_id.courseNum)
        return render(request, "attendance_complain.html", {"att": att})
    else:
        return redirect("/chosen_course/")


@is_login
def complain_process(request):
    if request.method == 'POST':
        email = request.COOKIES["qwer"]
        student_model = UserInfo.objects.get(email=email)
        attendance_id = request.POST.get("attendance_id")
        complain_words = request.POST.get("complain_words")
        # print(complain_words)
        att = AttendanceInfo.objects.filter(attendance_id=attendance_id)[0]
        complain_tag = attendance.objects.filter(stu=student_model, att=att)[0].complain_tag
        attendance.objects.filter(stu=student_model, att=att).update(complain_tag=str(int(complain_tag) + 1),
                                                                     complain_text=complain_words)
        stu_atten_results = []
        atten_info_results = AttendanceInfo.objects.filter(course_id=att.course_id.courseNum,
                                                           teacher_id=att.teacher_id.teacherNum)
        for row in atten_info_results:
            stu_atten_results.append(attendance.objects.filter(stu=student_model, att=row.attendance_id)[0])
        return render(request, "stu_check_atten.html",
                      {"stu_atten_results": stu_atten_results})

    else:
        return redirect("/chosen_course/")


@is_teacher_login
def deal_complain(request):
    email = request.COOKIES["qwer"]
    teacher_model = TeacherInfo.objects.get(email=email)
    complain_list = []
    att_info = AttendanceInfo.objects.filter(teacher_id=teacher_model)
    for row in att_info:
        att = attendance.objects.filter(att=row.attendance_id)
        for row_2 in att:
            comp = attendance.objects.filter(stu=row_2.stu, att=row_2.att)[0]
            if comp.complain_tag == '4':
                complain_list.append(comp)
    return render(request, "deal_complain.html", {"complain_list": complain_list})
