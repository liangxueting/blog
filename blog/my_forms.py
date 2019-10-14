from django import forms  #自动验证 forms组件
from django.forms import widgets
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from blog.models import Member
from django.forms import fields
from blog import models
# 用户表单的完善
class UserForm(forms.Form):

    member_name = fields.CharField()
    member_pwd = fields.CharField()
    r_pwd = fields.CharField()
    # 单独验证
    # 创建一个局部钩子
    def clean_member_name(self):
        member_name = models.Member.objects.filter(member_name=self.cleaned_data['member_name'])
        if not member_name:  #判断res是否存在，不存在则将用户的用户名返回给用户界面
            return self.cleaned_data
        else:
            # 当数据库中存在该用户名时，则返回用户名已存在
            raise ValidationError(':用户名已存在！')

    # 创建一个全局钩子
    def clean(self):
        member_pwd = self.cleaned_data['member_pwd']
        r_pwd = self.cleaned_data['r_pwd']

        if member_pwd and r_pwd:
            # 假设都有的情况下，判断密码与确认密码是否相同
            if member_pwd == r_pwd:
                # 密码与确认密码相同时返回给用户原信息
                return self.cleaned_data
            else:
                # 不存在时，返回给用户一个错误的提示(两次密码不一致)  注意用raise返回错误信息
                raise ValidationError('两次密码不一致！')
        else:
            return  self.cleaned_data
