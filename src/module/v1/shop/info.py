# -*- coding:utf-8 -*-

"""
店铺信息，包括创建店铺，获取店铺信息
@author fuweiyi
@time 2020/6/11
"""
from base.base import Base


class Controller(Base):

    auth = (('admin', 'platform'), )

    async def get(self):
        """
        获取指定店铺信息
        return data:
            {
                "admin_id": "",
                "account": "",
                "name": "",
            }
        """
        params = self.params()
        result = await self.cs('shop.service', 'query_info', params)
        self.out(result)

    async def post(self):
        """
        创建店铺
        @return:
        """
        params = self.params()
        result = await self.cs('shop.service', 'create_info', params)
        self.out(result)
