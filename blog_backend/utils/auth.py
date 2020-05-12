#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# Create: 2020-05-11 19:21:54
# Author: huihui - sunjiehuimail@foxmail.com
# Filename: auth.py


import json

from functools import wraps
from django_redis import get_redis_connection
from users.backend.users_backend import UserBKE
from django.conf import settings

def loginger(func):
    """
    登录装饰圈, 所有需要登录的视图装饰即可
    """
    @wraps(func)
    def inner(self, headers, **kwargs):
        ret = {
            "errcode": 10124,
            "errmsg": "Token无效"
        }
        try:
            token = headers.get("X-AUTH-USERTOKEN")
        except:
            return ret
        if not token:
            return ret

        # 本地验证
        # redis
        conn = get_redis_connection("default")
        if not conn.get("token_%s" % token):
            # mysql 防止redis挂掉
            user_obj = UserBKE.query_user_by_token(token=token)
            if not user_obj:
                """
                没有token
                """
                return ret
            user_obj = user_obj.first()

            user_dict = user_obj.to_dict()
        else:
            user_dict = json.loads(conn.get("token_%s" % token))
        headers["user_info"] = user_dict

        ret = func(self, headers, **kwargs)
        return ret

    return inner

def token_save_to_redis(token, data):
    """
    保存token到缓存
    """
    conn = get_redis_connection("default")
    conn.set("token_%s" % token, json.dumps(data), settings.TOKEN_OUTTIME)
    return True

def token_del_to_redis(token):
    """
    删除缓存中的token
    """
    conn = get_redis_connection("default")
    conn.delete("token_%s" % token)
    return True
