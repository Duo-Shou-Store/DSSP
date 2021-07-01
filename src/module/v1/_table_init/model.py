# -*- coding:utf-8 -*-

"""
@author: 萎迷一心
@time: 2021/7/1
"""
from source.async_model import AsyncModelBase


class Model(AsyncModelBase):

    async def execute(self, params):
        for l in params:
            for item in l:
                item = item.replace('\n', '')
                tx = await self.async_pools.begin()
                try:
                    await tx.execute(item)
                    await tx.commit()
                except Exception as e:
                    await tx.rollback()
                    self.logger.info(e.args)
