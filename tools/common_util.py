# -*- coding:utf-8 -*-

"""
@author: delu
@file: common_util.py
@time: 17/4/24 上午11:31
"""
import json
import cgi
import time
import hashlib
import random
import traceback
import re
from source.properties import Properties
from tools.logs import Logs

properties = Properties()
logger = Logs().logger


class CommonUtil(object):

    @classmethod
    def salt(cls, salt_len=6, is_num=False, chrset=''):
        """
        密码加密字符串
        生成一个固定位数的随机字符串，包含0-9a-z
        @:param salt_len 生成字符串长度
        """

        if is_num:
            chrset = '0123456789'
        else:
            if not chrset:
                chrset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWSYZ'
        salt = []
        for i in range(salt_len):
            item = random.choice(chrset)
            salt.append(item)

        return ''.join(salt)

    @classmethod
    def create_uuid(cls):
        """
        创建随机字符串
        :return:
        """
        text = str(time.time()) + cls.salt(12)
        m = hashlib.md5()
        m.update(bytes(text.encode(encoding='utf-8')))
        return m.hexdigest()

    @staticmethod
    def get_loader_version(path=None):
        """
        获取调用者的Version
        """
        version = None
        if path:
            version = re.findall(r"^v(.+?)\.", path)
            if version:
                version = 'v' + version[0]

        if not version:
            caller = traceback.extract_stack()[-3]
            caller_path = caller[0]
            version = re.findall(r"/src/module/(.+?)/", caller_path)
            if version:
                version = version[0]
        return version
