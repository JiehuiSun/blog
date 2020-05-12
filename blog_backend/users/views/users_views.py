#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# Create: 2020-05-08 11:07:26
# Author: huihui - sunjiehuimail@foxmail.com
# Filename: tags_views.py


import time
import json
import logging

from django_redis import get_redis_connection

from utils.auth import loginger, token_save_to_redis
from utils.helpers import (BaseViewTools, Resp, compose, gen_token, make_random_str)
from users.backend.users_backend import UserBKE

logger = logging.getLogger(__name__)

login_auth = compose(loginger)


class UsersLoginView(BaseViewTools):
    """
    用户账号登陆
    """
    # @login_auth
    def post(self, headers, data, files=None, key=None):
        params_dict = {
            "username": "required str",
            "password": "required str",
        }
        ret = self.ver_params(params_dict, data)
        if ret != True:
            return ret

        params = {
            "username": data["username"],
            "pwd": data["password"]
        }

        code, user_obj = UserBKE.ver_user_by_name(**params)
        if code != 1:
            return Resp.data(code)

        user_token = gen_token(user_obj.id,
                               make_random_str(4),
                               time.time())
        ret = dict()
        ret["token"] = user_token
        token_save_to_redis(user_token, user_obj.to_dict())

        return Resp.data(data=ret)


class UsersRegisterView(BaseViewTools):
    """
    用户账号注册
    """
    @login_auth
    def post(self, headers, data, files=None, key=None):
        params_dict = {
            "username": "required str",
            "alias": "required str",
            "password": "required str",
            "email": "optional str"
        }
        ret = self.ver_params(params_dict, data)
        if ret != True:
            return ret

        params = {
            "username": data["username"],
            "alias": data["alias"],
            "pwd": data["password"]
        }
        if data.get("email"):
            params["email"] = data["email"]

        code, user_obj = UserBKE.register_user(**params)
        if code != 1:
            return Resp.data(code)

        user_token = gen_token(user_obj.id,
                               make_random_str(4),
                               time.time())
        ret = dict()
        ret["token"] = user_token
        return Resp.data(data=ret)


class UserView(BaseViewTools):
    """
    用户
    """
    @login_auth
    def get(self, headers, data, files=None, key=None):
        params_dict = {
        }
        ret = self.ver_params(params_dict, data)
        if ret != True:
            return ret

        conn = get_redis_connection("default")
        if not conn.get("token_%s" % key):
            return Resp.data(10124)

        user_dict = json.loads(conn.get("token_%s" % key))
        return Resp.data(data=user_dict)
