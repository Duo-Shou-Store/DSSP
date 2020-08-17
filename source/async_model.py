# -*- coding:utf-8 -*-

import tormysql.cursor

from source.properties import properties
from source.sql_builder import SqlBuilder
from tools.date_json_encoder import CJsonEncoder
from tools.common_util import CommonUtil
from tools.date_utils import dateUtils
from tools.logs import logs


class AsyncModelBase(SqlBuilder):
    async_pools = tormysql.helpers.ConnectionPool(
        max_connections=int(properties.get('setting', 'mysql', 'MAX_CONNECTIONS')),
        idle_seconds=150,
        wait_connection_timeout=120,
        host=properties.get('setting', 'mysql', 'DB_HOST'),
        port=int(properties.get('setting', 'mysql', 'DB_PORT')),
        user=properties.get('setting', 'mysql', 'DB_USER'),
        passwd=properties.get('setting', 'mysql', 'DB_PASS'),
        db=properties.get('setting', 'mysql', 'DB_BASE'),
        charset="utf8mb4",
        cursorclass=tormysql.cursor.DictCursor,
    )

    date_encoder = CJsonEncoder
    util = CommonUtil
    date_utils = dateUtils
    logger = logs
    # tx = None

    def __init__(self):
        self.tx = None

    async def do_sqls(self, params_list):
        sql = ''
        tx = None
        result = None
        try:
            tx = await self.async_pools.begin()
            for params in params_list:

                sql_type = params[self.sql_constants.SQL_TYPE]
                table_name = params[self.sql_constants.TABLE_NAME]
                dict_data = params[self.sql_constants.DICT_DATA]
                value_tuple = params[self.sql_constants.VALUE_TUPLE]

                if sql_type == self.sql_constants.INSERT:
                    #  创建
                    sql = self.build_insert(table_name, dict_data)
                elif sql_type == self.sql_constants.BATCH_INSERT:
                    # 批量创建
                    sql = self.build_batch_insert(table_name, dict_data)
                elif sql_type == self.sql_constants.UPDATE:
                    # 更新
                    sql = self.build_update(table_name, dict_data)
                elif sql_type == self.sql_constants.DELETE:
                    # 删除
                    sql = self.build_delete(table_name, dict_data)

                await tx.execute(sql, value_tuple)
            if params_list:
                await tx.commit()
                result = True
        except Exception as e:
            await tx.rollback()
            self.logger.exception(e)
            self.logger.info(sql)
            result = None

        return result

    async def page_find(self, table_name, params, value_tuple, sql='', sql_count=''):
        """
        :param table_name:
        :param params:
        :param value_tuple:
        :param sql:
        :param sql_count:
        :return:
        """
        if not sql:
            sql = self.build_paginate(table_name, params)

        if not sql_count:
            sql_count = self.build_get_rows(table_name, params)

        result = None
        try:
            cursor = await self.async_pools.execute(sql, value_tuple)
            dict_list = cursor.fetchall()

            cursor = await self.async_pools.execute(sql_count, value_tuple)
            dic_rows = cursor.fetchone()
            result = {
                'list': dict_list,
                'row_count': dic_rows[self.sql_constants.ROW_COUNT] if dic_rows else 0
            }
        except Exception as e:
            self.logger.info(sql)
            self.logger.info(sql_count)
            self.logger.exception(e)

        return result

    async def get_rows(self, table_name, params, value_tuple):
        sql_count = self.build_get_rows(table_name, params)
        result = 0
        try:
            cursor = await self.async_pools.execute(sql_count, value_tuple)
            dic_rows = cursor.fetchone()

            result = dic_rows[self.sql_constants.ROW_COUNT] if dic_rows else 0
        except Exception as e:
            self.logger.info(sql_count)
            self.logger.exception(e)

        return result

    async def find(self, table_name, params=None, value_tuple=(), str_type='one'):
        sql = self.build_select(table_name, params)
        result = False
        try:
            cursor = await self.async_pools.execute(sql, value_tuple)
            if str_type == self.sql_constants.LIST:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
        except Exception as e:
            self.logger.info(sql)
            self.logger.exception(e)

        return result

    async def insert(self, table_name, params, value_tuple, auto_commit=True):
        sql = self.build_insert(table_name, params)
        result = None
        tx = await self.async_pools.begin()

        try:
            if auto_commit:
                cursor = await tx.execute(sql, value_tuple)
                await tx.commit()
                tx = None
            else:
                cursor = await self.tx.execute(sql, value_tuple)

            result = self.sql_constants.SUCCESS.copy()
            result['last_id'] = cursor.lastrowid
            result['affected_rows'] = cursor.rowcount
        except Exception as e:
            tx.rollback()
            self.logger.info(sql)
            self.logger.exception(e)

        return result

    async def batch_insert(self, table_name, params, value_tuple, auto_commit=True):
        result = None
        sql = self.build_batch_insert(table_name, params)
        if not self.tx:
            self.tx = await self.async_pools.begin()
        try:
            if auto_commit:
                cursor = await self.tx.execute(sql, value_tuple)
                await self.tx.commit()
                self.tx = None
            else:
                cursor = await self.tx.execute(sql, value_tuple)
            result = self.sql_constants.SUCCESS.copy()
            result['affected_rows'] = cursor.rowcount
        except Exception as e:
            self.logger.info(sql)
            self.logger.exception(e)

        return result

    async def update(self, table_name, params, value_tuple, auto_commit=True):
        result = None
        sql = self.build_update(table_name, params)
        if not self.tx:
            self.tx = await self.async_pools.begin()
        try:
            if auto_commit:
                cursor = await self.tx.execute(sql, value_tuple)
                await self.tx.commit()
                self.tx = None
            else:
                cursor = await self.tx.execute(sql, value_tuple)
            result = cursor.rowcount
        except Exception as e:
            self.logger.info(sql)
            self.logger.exception(e)

        return result

    async def delete(self, table_name, params, value_tuple, auto_commit=True):
        sql = self.build_delete(table_name, params)
        result = None
        if not self.tx:
            self.tx = await self.async_pools.begin()
        try:
            if auto_commit:
                cursor = await self.tx.execute(sql, value_tuple)
                await self.tx.commit()
                self.tx = None
            else:
                cursor = await self.tx.execute(sql, value_tuple)
            result = cursor.rowcount
        except Exception as e:
            self.logger.info(sql)
            self.logger.exception(e)

        return result
