#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# Create: 2020-05-08 11:19:08
# Author: huihui - sunjiehuimail@foxmail.com
# Filename: helpers.py


import types
import random
import hashlib
import datetime

from django.conf import settings

class Resp:
    """
    返回封装
    """
    """
    状态码说明: xxxxx
    前三位: 模块, 第四位: 区域, 第五位: 编码
    100xx: 系统级
    109xx: 第三方
    101xx: 用户级
    """
    err_code_dict = {
        # 其他
        10099: "其他错误",  # 找不到错误码使用(正常不会出现)

        # 参数
        10001: "参数不完整",
        10002: "参数错误",
        10003: "上传失败, 不支持的文件格式",

        # 数据库
        10011: "数据不存在或已被删除",
        10012: "未知的数据库错误",
        10013: "其他模块的数据库错误",
        10014: "删除失败",
        10015: "数据错误",

        # 文案
        10021: "",

        # 第三方
        10901: "其他异常",
    }

    # 用户
    err_code_dict[10121] = "账号错误"
    err_code_dict[10122] = "密码错误"

    @classmethod
    def data(cls, errcode=0, errmsg="", data={}):
        ret = {
            "errcode": errcode,
            "errmsg": "OK",
            "data": data
        }

        if ret["errcode"] == 0:
            return ret

        if errcode not in cls.err_code_dict:
            ret["errcode"] = 10399
        if errmsg:
            ret["errmsg"] = "{0}({1})".format(cls.err_code_dict[ret["errcode"]], errmsg)
        else:
            ret["errmsg"] = cls.err_code_dict[ret["errcode"]]

        return ret


class BaseViewTools:
    """
    视图封装
    """
    def ver_params(self, params_dict, data):
        data_keys = set(data.keys())
        max_keys = set(params_dict.keys())
        # mini keys 判断
        min_keys = set()
        for k in max_keys:
            check_method = params_dict[k]
            if isinstance(check_method, types.FunctionType):
                continue
            params_dict_list = params_dict[k].split(' ')
            if 'optional' not in params_dict_list:
                min_keys.add(k)
        overflow_keys = data_keys - max_keys
        lack_keys = min_keys - data_keys

        # 验证后端需要的key 传递情况
        flag_keys_not_match = False
        errmsg_keys_not_match = ''
        if overflow_keys:
            flag_keys_not_match = True
            errmsg_keys_not_match += '请求参数中, 多余的key包括: '
            errmsg_keys_not_match += ', '.join([str(k) for k in overflow_keys])
        if lack_keys:
            flag_keys_not_match = True
            errmsg_keys_not_match += '请求参数中, 缺少的key包括: '
            errmsg_keys_not_match += ', '.join([str(k) for k in lack_keys])
        if flag_keys_not_match:
            ret = {
                "errcode": 10301,
                "errmsg": errmsg_keys_not_match
            }
            return ret

        # 根据params_dict 逐条验证参数.
        errmsg_keys_valid = []
        for k, v in data.items():
            flag = False
            msg = ''
            check_method = params_dict[k]
            # 执行用户自定义验证方法
            if isinstance(check_method, types.FunctionType):
                flag, msg = check_method(v, k)
            elif isinstance(check_method, str):
                check_method_list = check_method.split(' ')
                for item_method in check_method_list:
                    flag, msg = getattr(self, '_valid_'+item_method)(v, k)
                    if not flag:
                        break
                # 执行默认方法
            if not flag:
                errmsg_keys_valid.append(msg)
                continue
        if errmsg_keys_valid:
            errmsg = ' '.join(errmsg_keys_valid)
            ret = {
                "errcode": 10301,
                "errmsg": "参数错误: {0}".format(errmsg)
            }
            return ret
        return True

    def _valid_str(self, i, key_name=None):
        if isinstance(i, str):
            return True, 'OK'
        return False, key_name

    def _valid_required(self, i, key_name=None):
        '''
        该参数必须有值, 并且判断不能为 False
        '''
        if i or i == 0 or i == []:
            return True, key_name
        return False, key_name

    def _valid_optional(self, i, key_name=None):
        '''
        该参数可以不存在
        '''
        return True, 'OK'

    def _valid_pass(self, i, key_name=None):
        '''
        该参数必须存在, 但不需要验证
        '''
        return True, 'OK'

    def _valid_list(self, i, key_name=None):
        '''
        参数必须为list类型
        '''
        if isinstance(i, list):
            return True, 'OK'
        return False, '{0} 必须为list(array)类型, 谢谢配合!'.format(key_name)

    def _valid_int(self, i, key_name=None):
        '''
        参数必须为int类型
        '''
        if isinstance(i, int):
            return True, 'OK'
        return False, '{0} 必须为int(整型)类型, 谢谢配合!'.format(key_name)

    def _valid_date(self, i, key_name=None):
        '''
        参数必须为日期xxxx-xx-xx xx:xx:xx
        '''
        try:
            datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
            return True, 'OK'
        except:
            return False, '{0} 日期格式错误, 如: "xxxx-xx-xx xx:xx:xx", 谢谢配合!'.format(key_name)


def compose(*funs):
    def deco(f):
        for fun in reversed(funs):
            f = fun(f)
        return f
    return deco


class ModelBase:
    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            value = f.value_from_object(self)
            if f.name == "is_deleted":
                continue
            if isinstance(f, models.DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else ""

            data[f.name] = value
        return data


def encryption_pwd(user_id):
    auth_login_key = settings.LOGIN_AUTH_KEY
    auth_code1 = hashlib.sha256(str("{0}{1}".format(str(user_id), str(auth_login_key))).encode("utf8")).hexdigest()
    auth_code = hashlib.sha256(str("{0}{1}".format(str(auth_code1), str(auth_login_key))).encode("utf8")).hexdigest()
    return auth_code

def gen_token(user_id, random_str, timestamp):
    """
    算法登录验证
    :param user_id: integer
    :param random_str: string
    :param timestamp: integer
    :return: token: string
    """
    auth_login_key = settings.LOGIN_AUTH_KEY
    auth_code1 = hashlib.sha256(str("{0}{1}{2}".format(str(user_id), str(random_str), str(auth_login_key))).encode("utf8")).hexdigest()
    auth_code = hashlib.sha256(str("{0}{1}{2}".format(str(auth_code1), str(timestamp), str(auth_login_key))).encode("utf8")).hexdigest()

    ret_params = {
        "user_id": user_id,
        "random_str": random_str,
        "timestamp": timestamp,
        "auth_code": auth_code
    }

    return "{user_id}-{random_str}-{timestamp}-{auth_code}".format(**ret_params)

def make_random_str(random_num=10):
    """
    创建随机数
    """
    ret = ''
    for i in range(random_num):
        num = random.randint(0,9)
        alfa = chr(random.randint(97,122))
        alfa2 = chr(random.randint(65,90))
        s = random.choice([str(num), alfa, alfa2])
        ret = ret+s
    return str(ret)
