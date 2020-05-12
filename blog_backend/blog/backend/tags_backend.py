#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# Create: 2020-05-08 11:32:33
# Author: huihui - sunjiehuimail@foxmail.com
# Filename: tags_backend.py


from blog.models import TagsModel
class TagsBKE:
    @classmethod
    def list_obj(cls, name=None):
        query_set = TagsModel.objects.filter(is_deleted=False)

        if name:
            query_set = query_set.filter(name__icontains=name)

        return query_set

    @classmethod
    def create_obj(cls, user_id, name):
        params = {
            "name": name,
            "user_id": user_id
        }
        tag_obj = TagsModel.objects.create(**params)
        return tag_obj

    @classmethod
    def query_obj(cls, user_id, tag_id):
        params = {
            "user_id": user_id,
            "tag_id": tag_id
        }
        tag_obj = TagsModel.objects.filter(id=tag_id,
                                           user_id=user_id,
                                           is_deleted=False)
        if not tag_obj:
            return False
        return tag_obj.first()
