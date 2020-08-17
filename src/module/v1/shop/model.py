# -*- coding:utf-8 -*-

"""
@author fuweiyi
@time 2020/6/11
"""
from source.async_model import AsyncModelBase


class Model(AsyncModelBase):

    tbl_shop = 'tbl_sm_shop'
    tbl_shop_admin = 'tbl_sm_shop_admin'

    async def query_one(self, params):
        """
        查询店铺信息（单条）
        @param params:
        @return:
        """
        fields = []
        condition = '1 = 1'
        values = []

        #
        if not self.util.is_empty('shop_id', params):
            condition += ' and shop_id = %s'
            values.append(params['shop_id'])

        result = await self.find(self.tbl_shop, {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition
        }, tuple(values))
        return result

    async def create(self, params):
        """
        创建店铺
        同时会创建超管和管理员分组数据
        @param params:
        @return:
        """
        sql_list = []
        # 创建店铺
        key = 'shop_id, shop_name, logo_url, admin_id, create_time'
        val = '%s, %s, %s, %s, %s'
        value = (
            params['shop_id'],
            params['shop_name'],
            params['logo_url'],
            params['admin_id'],
            params['create_time'],
        )
        #
        sql_list.append({
            self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
            self.sql_constants.TABLE_NAME: self.tbl_shop,
            self.sql_constants.DICT_DATA: {
                self.sql_constants.KEY: key,
                self.sql_constants.VAL: val
            },
            self.sql_constants.VALUE_TUPLE: value
        })
        # 创建管理员
        key = 'shop_id, admin_id, group_id, create_time'

        result = await self.do_sqls(sql_list)
        return result
