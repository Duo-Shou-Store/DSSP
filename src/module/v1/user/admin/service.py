# -*- coding:utf-8 -*-

"""
@package:
@file: service.py
@author: yuiitsu
@time: 2020-05-26 23:14
"""
from base.service import ServiceBase


class Service(ServiceBase):

    async def query(self, params):
        """
        @param params:
        @return:
        """
        return self._e('SUCCESS')