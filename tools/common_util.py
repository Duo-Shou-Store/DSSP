# -*- coding:utf-8 -*-

"""
@author: delu
@file: common_util.py
@time: 17/4/24 上午11:31
"""
import time
import hashlib
import random
import shortuuid


class CommonUtil(object):

    @staticmethod
    def is_empty(keys, my_dict):
        """
        判断keys中的元素是否存在为空
        :param keys:
        :param my_dict:
        :return: True/False
        """
        if not isinstance(keys, (str, list)):
            return False

        if isinstance(keys, str):
            keys = [keys]

        for key in keys:
            if key not in my_dict or my_dict[key] == '':
                return True

        return False

    @staticmethod
    def salt(salt_len=6, is_num=False, chrset=''):
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

    @staticmethod
    def create_uuid():
        """
        创建随机字符串
        :return:
        """
        return shortuuid.uuid()

    @staticmethod
    def md5(text):
        """
        md5加密
        :param text:
        :return:
        """
        result = hashlib.md5(text.encode(encoding='utf-8'))
        return result.hexdigest()
