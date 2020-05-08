#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# Create: 2020-05-08 11:01:13
# Author: huihui - sunjiehuimail@foxmail.com
# Filename: router.py


MODEL_NAME = "blog"
VERSION = "v1"

routing_table = dict()

routing_table["/{0}/{1}/tags/".format(MODEL_NAME, VERSION)] = "LPC::blog.views.tags_views.TagsView()"
