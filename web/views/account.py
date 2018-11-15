#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
import shutil
from io import BytesIO
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from utils.check_code import create_validate_code
from repository import models
from ..forms.account import LoginForm
from ..forms.account import RegisterForm


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    """论坛登录"""
    if request.method == 'GET':
        obj = LoginForm()
        return render(request, 'login.html', {'obj': obj})
    else:
        input_code = request.POST.get('code')
        session_code = request.session.get('CheckCode')
        if input_code.upper() == session_code.upper():
            username = request.POST.get('user')
            user = models.UserInfo.objects.filter(username=username).values('nid','password', 'nickname', 'username', 'email',
                                                                            'avatar', 'blog__nid', 'blog__site').first()
            if user:
                passwd = request.POST.get('pwd')
                if user['password'] == passwd:
                    request.session['user_info'] = user
                    return redirect('/')
                else:
                    msg1 = '密码错误'
                    obj = LoginForm(request.POST)
                    return render(request, 'login.html', {'obj': obj, 'msg1': msg1})
            else:
                msg2 = '此账号不存在'
                obj = LoginForm(request.POST)
                return render(request, 'login.html', {'obj': obj, 'msg2': msg2})
        else:
            msg3 = '验证码错误'
            obj = LoginForm(request.POST)
            return render(request, 'login.html', {'obj': obj, 'msg3': msg3})


def registered(request):
    """论坛注册"""
    sess_code = request.session.get('code')
    print(type(sess_code))
    if request.method == 'GET':
        obj = RegisterForm(request)
        return render(request, 'registered.html', {'obj': obj, })
    # /static\Hydrangeas.jpg
    else:
        file_obj = request.FILES.get('avatar')
        if file_obj:
            file_path = os.path.join("static\\upimg", file_obj.name)  # static\6.jpg
            with open(file_path, 'wb') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
        obj = RegisterForm(request, request.POST, request.FILES)
        if obj.is_valid():
            if not file_obj:
                obj.cleaned_data['avatar'] = "\static\\upimg\default.png"
            obj.cleaned_data.pop('passwd2')
            obj.cleaned_data.pop('code')
            username = request.POST.get('username')
            user = models.UserInfo.objects.filter(username=username)
            email = request.POST.get('email')
            male = models.UserInfo.objects.filter(email=email)
            if user:
                msg = '用户已存在'
                return render(request, 'registered.html', {'obj': obj, 'msg': msg})
            elif male:
                msg1 = '邮箱已存在'
                return render(request, 'registered.html', {'obj': obj, 'msg1': msg1})
            # elif re_code != sess_code:
            #     msg = '验证码错误'
            #     return render(request, 'registered.html', {'obj': obj, 'msg2': msg})
            else:
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                if os.path.isdir(BASE_DIR + '\static\\temp'):
                    shutil.rmtree(BASE_DIR + '\static\\temp')
                models.UserInfo.objects.create(**obj.cleaned_data)
                return redirect('/index.html')
        return render(request, 'registered.html', {'obj': obj})


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.clear()

    return redirect('/')
