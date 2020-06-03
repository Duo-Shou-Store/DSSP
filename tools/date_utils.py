# -*- coding:utf-8 -*-

"""
@author: delu
@file: date_utils.py
@time: 17/5/2 下午5:44
"""
import time
import datetime
import calendar

from tools.logs import logs

logger = logs


class DateUtils(object):

    YYYY_MM_DD = '%Y-%m-%d'
    YYYY_MM_DD_HH_MM = '%Y-%m-%d %H:%M'
    YYYY_MM_DD_HH_MM_SS = '%Y-%m-%d %H:%M:%S'
    YYYY_MM_DD_HH_MM_STR = '%Y年%m月%d日 %H:%M'
    YYYY_MM_DD_HH_MM_SS_INT = '%Y%m%d%H%M%S'
    FOREVER_START_TIME = '2000-01-01 00:00:00'
    FOREVER_END_TIME = '3000-01-01 00:00:00'

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
        获取当前时间，yyyy-mm-dd H:M:S
        :return: 
        """
        if is_timestamp:
            return int(time.time())
        return DateUtils.format_time(time.time(), time_format)

    @staticmethod
    def date_time_now():
        return datetime.datetime.now()

    @staticmethod
    def timestamps_now():
        """
        获取当前时间戳
        :return:
        """
        return time.time()

    @staticmethod
    def str_to_time(date, format_date="%Y-%m-%d %H:%M:%S"):
        """ 
        将日期字符串转为时间戳
        :param date: string 时间字符串，如：2017-04-28 10:00:00
        :param format_date: 时间格式，默认为 '%Y-%m-%d %H:%M:%S'
        """
        try:
            time_array = time.strptime(date, format_date)
            time_str = str(time.mktime(time_array))
            return int(time_str.split('.')[0])
        except Exception as e:
            logger.exception(e)
            return 0

    @staticmethod
    def time_to_str(date_time, format_date='%Y-%m-%d %H:%M:%S'):
        """
        将日期转为字符串
        :param date_time: 
        :param format_date: 
        :return: 
        """
        return date_time.strftime(format_date)

    @staticmethod
    def add_minute(date_str, format_date='%Y-%m-%d %H:%M:%S', minutes=0):
        """
        增加分钟
        :param date_str: 日期字符串
        :param format_date:
        :param minutes: 增加的分钟
        :return: 
        """
        time_array = time.strptime(date_str, format_date)
        mytime = str(time.mktime(time_array)).split('.')[0]
        mytime = int(mytime) + (60 * minutes)
        return time.strftime(format_date, time.localtime(mytime))

    @staticmethod
    def add_second(date_str, format_date='%Y-%m-%d %H:%M:%S', seconds=0):
        """
        增加分钟
        :param date_str: 日期字符串
        :param format_date:
        :param seconds: 增加的秒数
        :return: 
        """
        time_array = time.strptime(date_str, format_date)
        mytime = str(time.mktime(time_array)).split('.')[0]
        mytime = int(mytime) + seconds
        return time.strftime(format_date, time.localtime(mytime))

    @staticmethod
    def get_year_and_month(n=0):

        now = datetime.datetime.now()
        this_year = int(now.year)
        this_mon = int(now.month)
        this_day = int(now.day)

        total_mon = this_mon + n

        if (total_mon > 0) and (total_mon < 12):
            days = str(DateUtils.get_days_of_month(this_year, total_mon))
            total_mon = DateUtils.add_zero(total_mon)

            if (this_day > 0) and (this_day < 10):
                this_day = DateUtils.add_zero(this_day)

            return this_year, total_mon, days, this_day

        else:
            i = total_mon/12
            j = total_mon % 12
            if j == 0:
                i -= 1
                j = 12
            this_year += i
            days = str(DateUtils.get_days_of_month(int(this_year), j))
            j = DateUtils.add_zero(j)
            if (this_day > 0) and (this_day < 10):
                this_day = DateUtils.add_zero(this_day)

            return int(this_year), str(j), days, this_day

    @staticmethod
    def get_days_of_month(year, mon):
        return calendar.monthrange(year, mon)[1]

    @staticmethod
    def add_zero(n):
        """
        add 0 before 0-9
        return 01-09
        :param n:
        :return:
        """
        nabs = abs(int(n))
        if nabs < 10:
            return "0" + str(nabs)
        else:
            return nabs

    @staticmethod
    def get_today_months(n=0):
        year, mon, d, day = DateUtils.get_year_and_month(n)
        arr = (year, mon, d, day)
        if int(day) < int(d):
            arr = (year, mon, day)
        return "-".join("%s" % i for i in arr)


dateUtils = DateUtils()


if __name__ == '__main__':
    # print DateUtils.add_minute(DateUtils.time_now(DateUtils.YYYY_MM_DD) + ' 00:00:00', minutes=25 * 60, type='str')
    # print(DateUtils.str_to_time(DateUtils.time_now()))
    DateUtils.str_to_time('3001-01-19 20:00:00')
    # from functools import reduce
    # add_minute = lambda x, y: DateUtils.add_minute(x, minutes=y)
    # print(reduce(add_minute, ['2018-01-01 00:00:01', 5, 10]))
    current_datetime = datetime.datetime.now()
    current_second = current_datetime.second
    next_datetime = current_datetime + datetime.timedelta(minutes=1)
    next_timestamp = time.mktime(next_datetime.timetuple())


