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

        sign_pwd = encryption_pwd(user_obj.id)
        if user_obj.pwd != sign_pwd:
            return 10122, "密码错误"

        return 1, user_obj
