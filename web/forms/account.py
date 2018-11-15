#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms import fields
from django.forms import widgets


class LoginForm(Form):
    """
    登录
    """
    user = fields.CharField(
        required=True,
        min_length=4,
        max_length=12,
        widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': '用户'}),
        error_messages={
            'required': '不能为空',
            'max_length': '最长12位',
            'min_length': '最短4位',
        },
    )
    pwd = fields.CharField(
        required=True,
        min_length=4,
        max_length=12,
        widget=widgets.TextInput(attrs={'class': "form-control", "type": "password", 'placeholder': '密码'}),
        error_messages={
            'required': '不能为空',
            'max_length': '最长12位',
            'min_length': '最短4位',
        },
    )

    code = fields.CharField(
        required=True,
        min_length=0,
        max_length=5,
        widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': '验证码'}),
        error_messages={
            'required': '不能为空',
            'max_length': '最长5位',
            'min_length': '最短0位',
        },
    )


class RegisterForm(Form):
    username = fields.CharField(
        required=True,
        min_length=4,
        max_length=12,
        widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': '用户'}),
        error_messages={
            'required': '不能为空',
            'max_length': '最长12位',
            'min_length': '最短4位',
        },
    )

    password = fields.CharField(
        required=True,
        min_length=4,
        max_length=12,
        widget=widgets.TextInput(attrs={'class': "form-control", "type": "password", 'placeholder': '密码'}),
        error_messages={
            'required': '不能为空',
            'max_length': '最长12位',
            'min_length': '最短4位',
        },
    )
    passwd2 = fields.CharField(
        required=True,
        min_length=4,
        max_length=12,
        widget=widgets.TextInput(attrs={'class': "form-control", "type": "password", 'placeholder': '密码'}),
        error_messages={
            'required': '不能为空',
            'max_length': '最长12位',
            'min_length': '最短4位',
        },
    )
    nickname = fields.CharField(
        required=True,
        min_length=2,
        max_length=8,
        widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': '昵称'}),
        error_messages={
            'required': '不能为空',
            'max_length': '最长8位',
            'min_length': '最短2位',
        },
    )

    email = fields.EmailField(widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': '邮箱'}),
                              error_messages={
                                  'required': '不能为空',
                                  'invalid': '邮箱格式错误',
                              },
                              )
    avatar = fields.FileField(required=False, widget=widgets.FileInput(
        attrs={'id': "imgSelect", 'class': "f1", 'style': "display: none"}))
    # 'style': "display: none",
    code = fields.CharField(
        required=True,
        min_length=0,
        max_length=5,
        widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': '验证码'}),
        error_messages={
            'required': '不能为空',
            'max_length': '最长5位',
            'min_length': '最短0位',
        },
    )

    def __init__(self, request, *args, **kwargs):
        super(registeredFrom, self).__init__(*args, **kwargs)
        self.request = request

    # def clean_code(self):
    #     input_code = self.cleaned_data['code']
    #     session_code = self.request.session.get('code')
    #     if input_code.upper() == session_code.upper():
    #         return input_code
    #     raise ValidationError('验证码错误')

    def clean(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('passwd2')
        if p1 == p2:
            # return self.cleaned_data
            return None
        # self.add_error(None,ValidationError('密码不一致'))
        self.add_error("passwd2", ValidationError('密码不一致'))
