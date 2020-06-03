# -*- coding:utf-8 -*-

"""
@package:
@file: model.py
@author: yuiitsu
@time: 2020-05-24 18:39
"""
from source.async_model import AsyncModelBase


class Model(AsyncModelBase):

    def __init__(self):
        #
        self.save_obj = {
            'admin_id': '',
            'account_type': '',
            'account': '',
            'password': '',
            'salt': '',
            'create_time': self.date_utils.time_now()
        }
        #
        self.query_obj = {
            'page_index': '1',
            'page_size': '10'
        }

    async def query_one(self, params):
        """
        获取一条数据
        :param params:
        :return:
        """
        fields = []
        condition = '1 = 1'
        values = []
        #
        if not self.util.is_empty('shop_id', params):
            condition += ' and shop_id = %s'
            values.append(params['shop_id'])
        #
        if not self.util.is_empty('account', params):
            condition += ' and account = %s'
            values.append(params['account'])

        result = await self.find('tbl_um_admin_account', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition
        }, tuple(values))
        return result

    async def query_list(self, params):
        """
        获取多条数据
        :param params:
        :return:
        """
        fields = []
        condition = '1 = 1'
        values = []
        #
        if not self.util.is_empty('shop_id', params):
            condition += ' and shop_id = %s'
            values.append(params['shop_id'])
        #
        if not self.util.is_empty('account', params):
            condition += ' and account = %s'
            values.append(params['account'])

        result = await self.find('tbl_um_admin_account', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition
        }, tuple(values), self.sql_constants.LIST)
        return result

    async def query_page(self, params):
        """
        分页获取数据
        :param params:
        :return:
        """
        fields = []
        condition = '1 = 1'
        values = []
        #
        if not self.util.is_empty('shop_id', params):
            condition += ' and shop_id = %s'
            values.append(params['shop_id'])
        #
        if not self.util.is_empty('account', params):
            condition += ' and account = %s'
            values.append(params['account'])

        result = await self.page_find('tbl_um_admin_account', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition,
            self.sql_constants.LIMIT: [params['page_index'], params['page_size']]
        }, tuple(values))
        return result

    async def create(self, params):
        """
        创建用户数据, 包括admin和admin_account
        :param params:
        :return:
        """
        sql_list = []
        # admin_account
        key = 'admin_id, account_type, account, password, salt, create_time'
        val = '%s, %s, %s, %s, %s, %s'
        value = (
            params['admin_id'],
            params['account_type'],
            params['account'],
            params['password'],
            params['salt'],
            params['create_time'],
        )
        sql_list.append({
            self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
            self.sql_constants.TABLE_NAME: 'tbl_um_admin_account',
            self.sql_constants.DICT_DATA: {
                self.sql_constants.KEY: key,
                self.sql_constants.VAL: val
            },
            self.sql_constants.VALUE_TUPLE: value
        })
        # admin
        key = 'admin_id, name'
        val = '%s, %s'
        value = (
            params['admin_id'],
            params['account']
        )
        sql_list.append({
            self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
            self.sql_constants.TABLE_NAME: 'tbl_um_admin',
            self.sql_constants.DICT_DATA: {
                self.sql_constants.KEY: key,
                self.sql_constants.VAL: val
            },
            self.sql_constants.VALUE_TUPLE: value
        })
        #
        result = await self.do_sqls(sql_list)
        return result
