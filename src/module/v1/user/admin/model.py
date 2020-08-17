# -*- coding:utf-8 -*-

"""
@package:
@file: model.py
@author: yuiitsu
@time: 2020-05-26 23:14
"""
from source.async_model import AsyncModelBase


class Model(AsyncModelBase):

    async def query_one_and_account(self, params):
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
        fields = [
            'a.admin_id',
            'a.name',
            'account.account'
        ]
        condition = '1 = 1'
        values = []
        #
        if not self.util.is_empty('shop_id', params):
            condition += ' and a.shop_id = %s'
            values.append(params['shop_id'])
        #
        if not self.util.is_empty('admin_id', params):
            condition += ' and a.admin_id = %s'
            values.append(params['admin_id'])

        join = [
            {
                self.sql_constants.TABLE_NAME: 'tbl_um_admin_account as account',
                self.sql_constants.JOIN_CONDITION: 'a.admin_id = account.admin_id'
            }
        ]

        result = await self.find('tbl_um_admin as a', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition,
            self.sql_constants.JOIN: join
        }, tuple(values))
        return result

    async def modify(self, params):
        """
        修改用户信息
        @param params:
        @return:
        """
        fields = [
            'name = %s'
        ]
        condition = 'admin_id = %s'
        values = [params['name'], params['admin_id']]
        #
        result = await self.update('tbl_um_admin', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition
        }, tuple(values))
        return result
