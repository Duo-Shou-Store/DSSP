# -*- coding:utf-8 -*-
"""
@author: onlyfu
@time: 2021/06/28
"""
from source.async_model import AsyncModelBase
from ._table._tbl_um_admin_account import Table as tbl_account
from ._table._tbl_um_admin_info import Table as tbl_info


class Model(AsyncModelBase):

    def __init__(self):
        self.account_object = tbl_account.get_object()
        self.info_object = tbl_info.get_object()

    async def query_single_account(self, params):
        """
        @param params:
        @return:
        """
        fields = []
        condition = '1 = 1'
        values = []

        if 'account' in params and params['account']:
            condition += ' and account = %s '
            values.append(params['account'])

        if 'admin_id' in params and params['admin_id']:
            condition += ' and admin_id = %s '
            values.append(params['admin_id'])

        result = await self.find('tbl_um_admin_account', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition,
        }, tuple(values))
        return result

    async def query_single_admin_info(self, params):
        """
        @param params:
        @return:
        """
        fields = []
        condition = '1 = 1'
        values = []

        if 'admin_id' in params and params['admin_id']:
            condition += ' and admin_id = %s '
            values.append(params['admin_id'])

        result = await self.find('tbl_um_admin_info', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition,
        }, tuple(values))
        return result

    async def query_single_admin_full(self, params):
        """
        包含account和info信息
        @param params:
        @return:
        """
        fields = [
            'account.admin_id',
            'account.account',
            'account.password',
            'account.salt',
            'account.account_type',
            'info.name',
            'info.group_id',
            'info.mobile_number',
            'info.status',
            'info.create_time',
            'info.last_update_time',
        ]
        condition = '1 = 1'
        values = []

        if 'account' in params and params['account']:
            condition += ' and account.account = %s '
            values.append(params['account'])

        if 'admin_id' in params and params['admin_id']:
            condition += ' and account.admin_id = %s '
            values.append(params['admin_id'])

        join = [
            {
                self.sql_constants.TABLE_NAME: 'tbl_um_admin_info as info',
                self.sql_constants.JOIN_CONDITION: 'account.admin_id = info.admin_id'
            }
        ]

        result = await self.find('tbl_um_admin_account as account', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition,
            self.sql_constants.JOIN: join
        }, tuple(values))
        return result
