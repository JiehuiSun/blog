#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# Create: 2020-05-07 16:47:35
# Author: huihui - sunjiehuimail@foxmail.com
# Filename: dev.py

from .base import *


# 数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# 校验值
LOGIN_AUTH_KEY = "xiaohuihui"

# 缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:123456@172.17.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Token失效
TOKEN_OUTTIME = 24 * 60 * 60
