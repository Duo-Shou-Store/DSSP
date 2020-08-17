# -*- coding:utf-8 -*-
# WEB 入口文件
# 通过web/conf/route.py文件来配置路由
from __future__ import absolute_import

import os
import sys


parent_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(parent_path)
sys.path.append(parent_path)
sys.path.append(root_path)


import tornado.web
from route import route, power
from source.controller import Server
from src.config import CONF

print('Server started')

if __name__ == '__main__':
    Server.start(route, CONF)
else:
    app = tornado.web.Application(route, **CONF)
