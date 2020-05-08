#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# Create: 2020-05-08 11:28:22
# Author: huihui - sunjiehuimail@foxmail.com
# Filename: tags_models.py


from django.db import models
from utils.helpers import ModelBase


class UserBaseModel(models.Model, ModelBase):
    name = models.CharField(max_length=32, verbose_name="用户名")  # 英文数字下划线
    alias = models.CharField(max_length=32, verbose_name="别名")
    pwd = models.CharField(max_length=32, verbose_name="密码")
    email = models.CharField(max_length=32, verbose_name="邮箱")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    dt_created = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="创建时间")
    dt_updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")
