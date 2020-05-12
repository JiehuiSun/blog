#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# Create: 2020-05-08 11:07:26
# Author: huihui - sunjiehuimail@foxmail.com
# Filename: tags_views.py


import logging

from utils.helpers import BaseViewTools, Resp, compose
from blog.backend.tags_backend import TagsBKE

logger = logging.getLogger(__name__)

login_auth = compose()


class TagsView(BaseViewTools):
    """
    标签
    """
    @login_auth
    def list(self, headers, data, files=None, key=None):
        params_dict = {
            "name": "optional str",
        }
        ret = self.ver_params(params_dict, data)
        if ret != True:
            return ret

        params = dict()
        if data.get("name"):
            params["name"] = data["name"]

        tags_obj_list = TagsBKE.list_obj(*params)
        ret = dict()
        if not tags_obj_list:
            ret["data_list"] = list()
            return Resp.data(data=ret)

        ret["data_list"] = [i.to_dict() for i in tags_obj_list]

        return Resp.data(data=ret)
