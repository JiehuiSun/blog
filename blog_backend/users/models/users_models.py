#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# Create: 2020-05-08 11:28:22
# Author: huihui - sunjiehuimail@foxmail.com
# Filename: tags_models.py


from django.db import models


class ModelBase:
    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            value = f.value_from_object(self)
            if f.name == "is_deleted":
                continue
            if isinstance(f, models.DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else ""

            data[f.name] = value
        return data


class UserBaseModel(models.Model, ModelBase):
    name = models.CharField(max_length=32, verbose_name="用户名")  # 英文数字下划线
    alias = models.CharField(max_length=32, verbose_name="别名")
    pwd = models.CharField(max_length=64, verbose_name="密码")
    email = models.CharField(null=True, max_length=32, verbose_name="邮箱")
    avatar = models.CharField(null=True, max_length=256, verbose_name="头像")
    token = models.CharField(max_length=128, verbose_name="Token")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    dt_created = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="创建时间")
    dt_updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")
