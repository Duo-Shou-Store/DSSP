# -*- coding:utf-8 -*-

"""
数据库表初始化
@author: onlyfu
@time: 2021/4/1
"""
from source.properties import properties
from base.service import ServiceBase
from .model import Model


class Service(ServiceBase):

    def __init__(self):
        self.model = Model()

    async def execute(self, params):
        await self.model.execute(params)
        return self._rs()
