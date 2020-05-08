#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# Create: 2020-05-08 11:07:26
# Author: huihui - sunjiehuimail@foxmail.com
# Filename: tags_views.py


import time
import logging

from utils.helpers import BaseViewTools, Resp, compose, gen_token, make_random_str
from users.backend.users_backend import UserBKE

logger = logging.getLogger(__name__)

login_auth = compose()


class UsersLoginView(BaseViewTools):
    """
    用户账号登陆
    """
    @login_auth
    def post(self, headers, data, files=None, key=None):
        params_dict = {
            "username": "required str",
            "password": "required str",
        }
        ret = self.ver_params(params_dict, data)
        if ret != True:
            return ret

        params = {
            "user_name": data["username"],
            "pwd": data["password"]
        }

        code, user_obj = UserBKE.ver_user_by_name(*params)
        if code != 1:
            return Resp.data(code)

        user_token = gen_token(user_obj.id,
                               make_random_str(4),
                               time.time())
        ret = dict()
        return Resp.data(data=ret)
