# -*- encoding=utf-8 -*

import importlib
import os
import re

from django.conf import settings

"""
每个应用自建router.py文件，按照如下方式注册自己的 api url 和 回调函数/接口到路由表 routing_table；
key：为请求 url 路径，以 app 应用名开始，后面的路径自定义，需要注意末尾的 /，path 最好都统一以 / 结尾；
     url 在实际使用时前面需要加 "/api"，例如下面的例子中前端调用时 url 为 /api/goods/course/;
value：为回调函数或接口，当为本地回调函数时，以 LPC:: 开头，当为接口是以 URL:: 开头
     LPC:: 后面写调用 class 的路径（class的上一层必须是一个module），URL:: 后写 http 调用地址

routing_table = {
    '/goods/course/': 'LPC::goods.views.CourseView',      # 支持 classmethod 和 staticmethod 方法
    '/goods/service/': 'LPC::goods.views.ServiceView()',  # 加()表示支持实例化方法
    '/trade/order/': 'URL::http://trade.mumway.com/order',
}

按照上面的路由配置：
1、若请求url为 /api/goods/course/，网关会调用 goods.views.CourseView.list 方法；
2、若请求url为 /api/goods/course/2/，网关会调用 goods.views.CourseView.get 方法, 2会赋值给get方法的key参数
"""

routing_table = {}
re_routing_list = []

for app in settings.INSTALLED_APPS:
    if app.startswith('django') or app.startswith('rest_framework') or app.startswith('gateway'):
        continue
    if os.path.exists(os.path.join(settings.BASE_DIR, '{}/router.py'.format(app))):
        app_router = importlib.import_module('{}.router'.format(app))
        routing_table.update(app_router.routing_table)
        if hasattr(app_router, 're_routing_table'):
            for k, v in app_router.re_routing_table.items():
                re_routing_list.append((re.compile(k), v))

