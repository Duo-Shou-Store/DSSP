# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/8/31
"""
from source.async_model import AsyncModelBase


class Model(AsyncModelBase):

    async def query(self, params):
        fields = []
        result = await self.find('tbl_cfg_admin', {
            self.sql_constants.FIELDS: fields
        })
        return result
