# -*- coding:utf-8 -*-

"""
系统初始化
- 创建配置文件
- 创建数据库及表
- 创建默认数据
@package:
@file: init.py
@author: yuiitsu
@time: 2020-05-24 14:14
"""
import os
import sys


parent_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(parent_path)
sys.path.append(parent_path)
sys.path.append(root_path)


import asyncio
from update.update_sql import Model


def run():
    # 获取参数
    arguments = sys.argv
    for k, v in enumerate(arguments):
        if v == '-t':
            loop_num = arguments[k + 1]

        if v == '-c':
            config_file = arguments[k + 1]

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(Model().execute_sql())


if __name__ == '__main__':
    run()
