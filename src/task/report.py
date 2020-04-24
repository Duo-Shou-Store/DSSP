# -*- coding: utf-8 -*-

"""
@author: Yuiitsu
@file: report
@time: 2018/7/13 16:32
"""
from email.message import EmailMessage
from tornado_smtp.client import TornadoSMTP

from source.properties import properties
from tools.date_utils import DateUtils
from tools.logs import logs

date_utils = DateUtils()
logger = logs.logger


class Report:

    send_time = 0
    smtp_server = properties.get('task', 'smtp', 'server')
    smtp_account = properties.get('task', 'smtp', 'account')
    smtp_pass = properties.get('task', 'smtp', 'pass')
    report_from = properties.get('task', 'report', 'from')
    report_to = properties.get('task', 'report', 'to')
    report_server = properties.get('task', 'report', 'server')

    @classmethod
    async def report(cls, content, error_track):
        """
        发送错误邮件
        :param content: 邮件内容
        :param error_track: 错误信息
        :return:
        """
        timestamps_now = date_utils.timestamps_now()
        if cls.send_time + 1800 <= timestamps_now:
            logger.info('send report message. error: %s', error_track)
            # 发送邮件
            smtp = TornadoSMTP(cls.smtp_server, use_ssl=True)
            # await smtp.starttls()
            await smtp.login(cls.smtp_account, cls.smtp_pass)

            msg = EmailMessage()
            msg['Subject'] = '[{}]Task error.'.format(cls.report_server)
            msg['To'] = cls.report_to
            msg['From'] = cls.report_from
            msg.set_content(error_track, 'html', 'utf-8')

            await smtp.send_message(msg)

            cls.send_time = timestamps_now
