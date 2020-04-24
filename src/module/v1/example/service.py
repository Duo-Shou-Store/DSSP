# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/8/31
"""
from base.service import ServiceBase
from .model import Model


class Service(ServiceBase):

    def __init__(self):
        self.model = Model()

    async def query(self, params):
        data = await self.model.query({})
        return self._grs(data)
