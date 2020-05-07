# -*- encoding=utf-8 -*-

import json
import requests
import importlib
from urllib.parse import urljoin

from django.http import JsonResponse, HttpResponseServerError, HttpResponseNotFound, HttpResponseBadRequest
import logging
from rest_framework.views import APIView

from .router import routing_table, re_routing_list

logger = logging.getLogger(__name__)
METHOD_MAP = {
    'get': requests.get,
    'post': requests.post,
    'put': requests.put,
    'patch': requests.patch,
    'delete': requests.delete
}


class GateWay(APIView):
    # comment this line to open the sign verification
    # authentication_classes = ()

    def __get_subpath(self, path):
        tail_slash = ''
        if path.endswith('/'):
            path = path[:-1]
            tail_slash = '/'
        path, key = path.rsplit('/', maxsplit=1)
        path += '/'
        return path, key, tail_slash

    def __load_class(self, class_path):
        pos = class_path.rfind('.')
        module_path = class_path[:pos]
        class_name = class_path[pos + 1:]
        mod = importlib.import_module(module_path)
        cls = getattr(mod, class_name)
        return cls

    def __dispatch(self, request):
        path = request.path.replace('/api', '')
        if not path:
            return HttpResponseNotFound()
        key = None
        path_dict = {}
        tail_slash = ''
        api_path = path
        upstream = ''
        if path in routing_table:
            upstream = routing_table[path]
        else:
            subpath, key, tail_slash = self.__get_subpath(path)
            if subpath in routing_table:
                upstream = routing_table[subpath]
                api_path = subpath
            else:
                for re_obj, call_addr in re_routing_list:
                    ret = re_obj.search(path)
                    if ret:
                        upstream = call_addr
                        path_dict = ret.groupdict()
                        break
        if not upstream:
            return HttpResponseNotFound()

        lpc = ''
        url = ''
        if upstream.startswith('LPC::'):
            lpc = upstream.replace('LPC::', '')
        elif routing_table[path].startswith('URL::'):
            url = upstream.replace('URL::', '')
            if key:
                url = urljoin(url, "/{0}{1}".format(key, tail_slash))
        else:
            return HttpResponseServerError()

        headers = {
            'Host': request.META['HTTP_HOST'],
            'User-Agent': request.META['HTTP_USER_AGENT'],
            'X-Real-IP': request.META['REMOTE_ADDR'],
            'Path': api_path,
            'Dev-Platform': request.META.get('HTTP_DEV_PLATFORM', None),
            'Dev-Model': request.META.get('HTTP_DEV_MODEL', None),
            'Dev-Version': request.META.get('HTTP_DEV_VERSION', None),
            'App-Version': request.META.get('HTTP_APP_VERSION', None),
            'App-Client': request.META.get('HTTP_APP_CLIENT', None),
            'App-Id': request.META.get('HTTP_X_AUTH_APPID', None),
            'Path_Dict': path_dict,
        }
        if 'HTTP_X_AUTH_USERTOKEN' in request.META:
            headers['X-AUTH-USERTOKEN'] = request.META['HTTP_X_AUTH_USERTOKEN']
        for k, v in request.FILES.items():
            request.data.pop(k)
        if request.content_type and request.content_type.lower() == 'application/json':
            headers['Content-Type'] = request.content_type

        if request.method.lower() == 'get':
            data = request.GET
        else:
            data = request.data

        if lpc:
            need_instance = False
            if lpc.endswith('()'):
                need_instance = True
                lpc = lpc.replace('()', '')
            module = self.__load_class(lpc)
            try:
                call_method = request.method.lower()
                if call_method == 'get' and not key:
                    call_method = 'list'
                if need_instance:
                    method = getattr(module(), call_method)
                else:
                    method = getattr(module, call_method)
            except AttributeError:
                return HttpResponseBadRequest()
            res = method(headers=headers, data=data, files=request.FILES, key=key) or {}
            return JsonResponse(data=res, status=200)
        if url:
            return METHOD_MAP[request.method.lower()](url, headers=headers, data=data, files=request.FILES)

    def get(self, request):
        return self.__dispatch(request)

    def post(self, request):
        return self.__dispatch(request)

    def put(self, request):
        return self.__dispatch(request)

    def patch(self, request):
        return self.__dispatch(request)

    def delete(self, request):
        return self.__dispatch(request)
