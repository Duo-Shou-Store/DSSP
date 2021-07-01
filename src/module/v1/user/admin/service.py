# -*- coding:utf-8 -*-

"""
@author: onlyfu
@time: 2017/12/4 17:20
"""
import tornado.gen
from base.service import ServiceBase
from .model import Model


class Service(ServiceBase):

    def __init__(self):
        self.model = Model()

    async def query_single_account(self, params):
        """
        查询一个帐号信息，只含帐号信息，不含管理员其它信息
        @param params:
            params['account']
            params['admin_id']
        @return:
        """
        if self.common_utils.is_empty(['account'], params) \
                and self.common_utils.is_empty(['admin_id'], params):
            self._end('PARAMS_NOT_EXIST')

        data = await self.model.query_single_account(params)
        if not data:
            return self._e('DATA_NOT_EXIST')

        return self._rs(data)

    @ServiceBase.params_set('model', 'info_object')
    async def query_single_admin_info(self, params):
        """
        查询一个管理员信息，不今帐号信息
        @param params:
            params['admin_id']
        @return:
        """
        if self.common_utils.is_empty(['admin_id'], params):
            self._end('PARAMS_NOT_EXIST')

        data = await self.model.query_single_admin_info(params)
        if not data:
            return self._e('DATA_NOT_EXIST')

        return self._rs(data)

    async def query_single_admin_full(self, params):
        """
        查询一个管理员信息，包含account和info信息
        @param params:
            params['account']
            params['admin_id']
        @return:
        """
        if self.common_utils.is_empty(['account'], params) \
                and self.common_utils.is_empty(['admin_id'], params):
            self._end('PARAMS_NOT_EXIST')

        data = await self.model.query_single_admin_full(params)
        if not data:
            return self._e('DATA_NOT_EXIST')

        return self._rs(data)

    async def create_admin(self, params):
        """
        创建管理员，包含Account和info信息
        @param params:
            params['account'] (*)
            params['password'] (*)
            params['name'] (*)
            params['group_id'] (*)
        @return:
        """
        if self.common_utils.is_empty(['account', 'password', 'name', 'group_id'], params):
            self._end('PARAMS_NOT_EXIST')

        # if self.body_is_empty(['account', 'password', 'name', 'group_id']):
        #     pass

        # check group

        # 账号是否可以注册
        account_result = await self.query_single_account(params)
        if account_result['code'] == 0:
            self._end('DATA_EXIST')
        #
        # salt = self.salt()
        # password = self.md5(self.md5(params['password']) + salt)
        # params['password'] = password
        # params['salt'] = salt
        # # result = yield self.model.create_info(params)
        # result = {}
        #
        # if result is None:
        #     raise self._gre('SQL_EXECUTE_ERROR')
        # else:
        #     raise self._grs(result)

    async def delete_info(self, params):
        """
        @param params:
        @return:
        """
        return self._rs()

    async def modify_info(self, params):
        """
        @param params:
        @return:
        """
        return self._rs()
