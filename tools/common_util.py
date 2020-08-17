# -*- coding:utf-8 -*-

"""
@author onlyfu
@file: common_util.py
@time 2020/6/2
"""
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

    @staticmethod
    def check_password_level(password):
        """
        检查密码强度
        @param password:
        @return:
        """
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        lower_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                         'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        upper_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                         'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        special_characters = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+',
                              '_', ';', ':', ',', '.', '/', '?', '[', ']', '\\', '|']

        #
        s = list(password)
        for item in s:
            if item not in numbers and item not in lower_letters and item not in upper_letters and \
                    item not in special_characters:
                return 0

        return 1
