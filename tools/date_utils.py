# -*- coding:utf-8 -*-

"""
@author: onlyfu
@file: date_utils.py
@time: 2020/6/2
"""
import time

from tools.logs import logs

logger = logs


class DateUtils(object):

    @staticmethod
    def format_time(timestamp, time_format='%Y-%m-%d %H:%M:%S'):
        """
        将时间戳格式化为时间字符串
        :param timestamp: int 时间戳
        :param time_format: string 时间格式，默认为 '%Y-%m-%d %H:%M:%S'
        :return:
        """
        return time.strftime(time_format, time.localtime(timestamp))

    @staticmethod
    def time_now(time_format='%Y-%m-%d %H:%M:%S', is_timestamp=False):
        """
        获取当前时间，YYYY-mm-dd H:M:S
        :return: 
        """
        if is_timestamp:
            return int(time.time())

        return DateUtils.format_time(time.time(), time_format)

    @staticmethod
    def timestamps_now():
        """
        获取当前时间戳
        :return:
        """
        return time.time()


dateUtils = DateUtils
