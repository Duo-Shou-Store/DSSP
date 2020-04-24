# -*- coding:utf-8 -*-

import tornado.gen
import tornado_mysql
from tornado_mysql import pools

from source.properties import properties
from source.sql_builder import SqlBuilder
from source.sql_builder_orm import SqlBuilderOrm
from tools.date_json_encoder import CJsonEncoder
from tools.common_util import CommonUtil
from tools.date_utils import DateUtils
from tools.logs import logs


class AsyncModelBase(SqlBuilder):
    async_pools = pools.Pool(dict(
        host=properties.get('setting', 'mysql', 'DB_HOST'),
        port=int(properties.get('setting', 'mysql', 'DB_PORT')),
        user=properties.get('setting', 'mysql', 'DB_USER'),
        passwd=properties.get('setting', 'mysql', 'DB_PASS'),
        db=properties.get('setting', 'mysql', 'DB_BASE'),
        charset='utf8',
        autocommit=False,
        cursorclass=tornado_mysql.cursors.DictCursor
    ),
        max_idle_connections=5,
        max_open_connections=int(properties.get('setting', 'mysql', 'MAX_CONNECTIONS')),
        max_recycle_sec=int(properties.get('setting', 'mysql', 'MAX_RECYCLE_SEC'))
    )

    tx = None
    sql_builder_orm = None
    if not sql_builder_orm:
        sql_builder_orm = SqlBuilderOrm()

    properties = properties
    date_encoder = CJsonEncoder
    util = CommonUtil
    date_utils = DateUtils
    logger = logs.logger

    async def do_sqls(self, params_list):
        # 执行多条sql
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
                yield tx.commit()
                # result = self._gr(self.sql_constants.SUCCESS.copy())
                result = self._gr(True)
        except Exception as e:
            yield tx.rollback()
            self.logger.exception(e)
            self.logger.info(sql)
            raise self._gr(None)
        raise result

    @tornado.gen.coroutine
    def page_find(self, table_name, params, value_tuple):
        """
        分页查询
        :param params: 
        :return: 
        """
        # 分页查询
        sql = self.build_paginate(table_name, params)
        sql_count = self.build_get_rows(table_name, params)
        result = None
        try:
            cursor = yield self.async_pools.execute(sql, value_tuple)
            dict_list = cursor.fetchall()

            cursor = yield self.async_pools.execute(sql_count, value_tuple)
            dic_rows = cursor.fetchone()
            result = {
                'list': dict_list,
                'row_count': dic_rows[self.sql_constants.ROW_COUNT] if dic_rows else 0
            }
        except Exception as e:
            self.logger.info(sql)
            self.logger.info(sql_count)
            self.logger.exception(e)
        raise self._gr(result)

    @tornado.gen.coroutine
    def get_rows(self, table_name, params, value_tuple):
        """
        统计数量
        :param params: 
        :return: 
        """
        sql_count = self.build_get_rows(table_name, params)
        result = 0
        try:
            cursor = yield self.async_pools.execute(sql_count, value_tuple)
            dic_rows = cursor.fetchone()

            result = dic_rows[self.sql_constants.ROW_COUNT] if dic_rows else 0
        except Exception as e:
            self.logger.info(sql_count)
            self.logger.exception(e)
        raise self._gr(result)

    @tornado.gen.coroutine
    def find(self, table_name, params={}, value_tuple=(), str_type='one'):
        """
        查询
        :param params: 
        :return: 
        """
        sql = self.build_select(table_name, params)
        result = False
        try:
            cursor = yield self.async_pools.execute(sql, value_tuple)
            if str_type == self.sql_constants.LIST:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
        except Exception as e:
            self.logger.info(sql)
            self.logger.exception(e)
        raise self._gr(result)

    @tornado.gen.coroutine
    def insert(self, table_name, params, value_tuple, auto_commit=True):
        """
        创建
        :param params: 
        :return: 
        """
        sql = self.build_insert(table_name, params)
        result = None
        if not self.tx:
            self.tx = yield self.async_pools.begin()
        try:
            if auto_commit:
                cursor = yield self.tx.execute(sql, value_tuple)
                yield self.tx.commit()
                self.tx = None
            else:
                cursor = yield self.tx.execute(sql, value_tuple)
            id = cursor.lastrowid
            result = self.sql_constants.SUCCESS.copy()
            result['last_id'] = id
            result['affected_rows'] = cursor.rowcount
        except Exception as e:
            self.tx.rollback()
            self.logger.info(sql)
            self.logger.exception(e)
        raise self._gr(result)

    @tornado.gen.coroutine
    def batch_insert(self, table_name, params, value_tuple, auto_commit=True):
        """
        批量插入
        :param table_name: 
        :param params: 
        :param value_tuple: 
        :param auto_commit: 
        :return: 
        """
        result = None
        sql = self.build_batch_insert(table_name, params)
        if not self.tx:
            self.tx = yield self.async_pools.begin()
        try:
            if auto_commit:
                cursor = yield self.tx.execute(sql, value_tuple)
                yield self.tx.commit()
                self.tx = None
            else:
                cursor = yield self.tx.execute(sql, value_tuple)
            result = self.sql_constants.SUCCESS.copy()
            result['affected_rows'] = cursor.rowcount
        except Exception as e:
            self.logger.info(sql)
            self.logger.exception(e)
        raise self._gr(result)

    @tornado.gen.coroutine
    def update(self, table_name, params, value_tuple, auto_commit=True):
        """
        更新
        :param params: 
        :return: 
        """
        result = None
        sql = self.build_update(table_name, params)
        if not self.tx:
            self.tx = yield self.async_pools.begin()
        try:
            if auto_commit:
                cursor = yield self.tx.execute(sql, value_tuple)
                yield self.tx.commit()
                self.tx = None
            else:
                cursor = yield self.tx.execute(sql, value_tuple)
            # result = self.sql_constants.SUCCESS.copy()
            # result['affected_rows'] = cursor.rowcount
            result = cursor.rowcount
        except Exception as e:
            self.logger.info(sql)
            self.logger.exception(e)
        raise self._gr(result)

    @tornado.gen.coroutine
    def delete(self, table_name, params, value_tuple, auto_commit=True):
        """`
        删除
        :param params: 
        :return: 
        """
        sql = self.build_delete(table_name, params)
        result = None
        if not self.tx:
            self.tx = yield self.async_pools.begin()
        try:
            if auto_commit:
                cursor = yield self.tx.execute(sql, value_tuple)
                yield self.tx.commit()
                self.tx = None
            else:
                cursor = yield self.tx.execute(sql, value_tuple)
            # result = self.sql_constants.SUCCESS
            # result['affected_rows'] = cursor.rowcount
            result = cursor.rowcount
        except Exception as e:
            self.logger.info(sql)
            self.logger.exception(e)

        raise self._gr(result)

    def _gr(self, result):
        """
        异步返回结果
        :param result: 
        :return: 
        """
        return tornado.gen.Return(result)
