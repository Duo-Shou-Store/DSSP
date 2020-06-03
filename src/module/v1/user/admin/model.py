# -*- coding:utf-8 -*-

"""
@package:
@file: model.py
@author: yuiitsu
@time: 2020-05-26 23:14
"""
from source.async_model import AsyncModelBase


class Model(AsyncModelBase):

    async def query_one(self, params):
        """
        获取一条用户信息记录
        :param params:
        :return:
            {
                id:
                admin_id:
                name:
            }
        """
        fields = []
        condition = '1 = 1'
        values = []
        #
        if not self.util.is_empty('shop_id', params):
            condition += ' and shop_id = %s'
            values.append(params['shop_id'])
        #
        if not self.util.is_empty('shop_id', params):
            condition += ' and shop_id = %s'
            values.append(params['shop_id'])
