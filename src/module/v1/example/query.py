# -*- coding:utf-8 -*-

"""
@author fuweiyi
@time 2020/4/17
"""
from base.base import Base


class Controller(Base):

    async def get(self):
        params = self.params()
        res = await self.do_service('example.service', 'update', params)
        self.out(res)
