# -*- coding:utf-8 -*-

"""
@package:
@file: return_code.py
@author: yuiitsu
@time: 2020-05-24 23:05
"""
from ..return_code import Code

Code.update({
    'CREATE_ACCOUNT_FAILED': {'code': 20101, 'msg': '创建帐号失败.'},
    'OLD_PASSWORD_NOT_MATCH': {'code': 20102, 'msg': '原密码错误.'},
    'PASSWORD_MISMATCH_RULES': {'code': 20103, 'msg': '密码不符合要求.'},
    'PASSWORD_LENGTH_ERROR': {'code': 20104, 'msg': '密码长度不符合要求.'},
})
