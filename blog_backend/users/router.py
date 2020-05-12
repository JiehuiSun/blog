#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# Create: 2020-05-08 18:01:13
# Author: huihui - sunjiehuimail@foxmail.com
# Filename: router.py


MODEL_NAME = "users"
VERSION = "v1"

routing_table = dict()

routing_table["/{0}/{1}/login/".format(MODEL_NAME, VERSION)] = "LPC::users.views.users_views.UsersLoginView()"
routing_table["/{0}/{1}/register/".format(MODEL_NAME, VERSION)] = "LPC::users.views.users_views.UsersRegisterView()"
routing_table["/{0}/{1}/user/".format(MODEL_NAME, VERSION)] = "LPC::users.views.users_views.UserView()"
