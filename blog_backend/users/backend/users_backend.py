#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# Create: 2020-05-08 17:32:33
# Author: huihui - sunjiehuimail@foxmail.com
# Filename: tags_backend.py


from users.models import UserBaseModel
from utils.helpers import encryption_pwd


class UserBKE:
    @classmethod
    def ver_user_by_name(cls, username, pwd):
        """
        params username: 用户名/邮箱
        params pwd: 明文密码
        return: code, msg/obj
        """
        query_set = UserBaseModel.objects.filter(is_deleted=False)

        query_set = query_set.filter(name=username)
        if not query_set:
            query_set = query_set.filter(email=username)
        if not query_set:
            return 10121, "账号错误"

        user_obj = query_set.first()

        sign_pwd = encryption_pwd(user_obj.name)
        if user_obj.pwd != sign_pwd:
            return 10122, "密码错误"

        return 1, user_obj

    @classmethod
    def register_user(cls, username, alias, pwd, email=None):
        """
        params username: 用户名/邮箱
        params alias: 别名
        params pwd: 明文密码
        return: code, msg/obj
        """
        query_set = UserBaseModel.objects.filter(is_deleted=False)

        query_set = query_set.filter(name=username)
        if not query_set:
            query_set = query_set.filter(email=username)

        if query_set:
            return 10123, "账号已存在"

        sign_pwd = encryption_pwd(username)
        params = {
            "name": username,
            "alias": alias,
            "pwd": sign_pwd,
        }
        if email:
            params["email"] = email

        user_obj = UserBaseModel.objects.create(**params)
        return 1, user_obj

    @classmethod
    def query_user_by_token(cls, token):
        """
        params token: 用户Token
        return user_obj
        """
        user_obj = UserBaseModel.objects.filter(is_deleted=False,
                                                token=token).first()
        if not user_obj:
            return False
        return user_obj
