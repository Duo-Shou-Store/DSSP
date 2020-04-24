# -*- coding:utf-8 -*-

"""
@author: onlyfu
@time: 20/04/17
"""
from base.base import Base


class Controller(Base):

    async def post(self):
        params = self.params()
        res = await self.do_service('example.service', 'update', params)
        self.out(res)
