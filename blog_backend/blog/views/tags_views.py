#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# Create: 2020-05-08 11:07:26
# Author: huihui - sunjiehuimail@foxmail.com
# Filename: tags_views.py


import logging

from django.db import transaction

from utils.auth import loginger
from utils.helpers import BaseViewTools, Resp, compose
from blog.backend.tags_backend import TagsBKE

logger = logging.getLogger(__name__)

login_auth = compose(loginger)


class TagsView(BaseViewTools):
    """
    标签
    """
    @login_auth
    def list(self, headers, data, files=None, key=None):
        params_dict = {
            "name": "optional str",
            "page_num": "optional str",
            "page_size": "optional str",
        }
        ret = self.ver_params(params_dict, data)
        if ret != True:
            return ret

        params = dict()
        if data.get("name"):
            params["name"] = data["name"]

        tags_obj_list = TagsBKE.list_obj(**params)
        ret = dict()
        if not tags_obj_list:
            ret["data_list"] = list()
            return Resp.data(data=ret)

        ret["data_list"] = [i.to_dict() for i in tags_obj_list]
        ret["total_size"] = 1

        return Resp.data(data=ret)

    @login_auth
    def post(self, headers, data, files=None, key=None):
        params_dict = {
            "name": "required str",
        }
        ret = self.ver_params(params_dict, data)
        if ret != True:
            return ret

        params = {
            "user_id": headers["user_info"]["id"],
            "name": data["name"]
        }

        with transaction.atomic():
            try:
                tag_obj = TagsBKE.create_obj(**params)
            except Exception as e:
                return Resp.data(10221, str(e))

        return Resp.data()

    @login_auth
    def delete(self, headers, data, files=None, key=None):
        params_dict = {
            "tag_id": "required int",
        }
        ret = self.ver_params(params_dict, data)
        if ret != True:
            return ret

        params = {
            "user_id": headers["user_info"]["id"],
            "tag_id": data["tag_id"]
        }
        tag_obj = TagsBKE.query_obj(**params)
        if not tag_obj:
            return Resp.data(10011)
        tag_obj.is_deleted = True
        tag_obj.save()

        return Resp.data()
