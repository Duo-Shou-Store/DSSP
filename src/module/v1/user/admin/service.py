# -*- coding:utf-8 -*-

"""
@package:
@file: service.py
@author: yuiitsu
@time: 2020-05-26 23:14
"""
from base.service import ServiceBase
from .model import Model
from .return_code import Code


class Service(ServiceBase):

    def __init__(self):
        self.model = Model()
        self.return_code = Code()

    async def query_info(self, params):
        """
        获取登录用户信息
        @param params:
        @return:
            {
                "admin_id": "",
                "name": "",
                "account": ""
            }
        """
        data = await self.model.query_one_and_account({
            'admin_id': self.user_data['admin_id']
        })
        if not data:
            data = {}

        return self._rs(data)

    async def modify_info(self, params):
        """
        修改登录用户的信息，可以修改：
            2. 昵称
        @param params:
            params['name']
        @return:
        """
        if self.common_utils.is_empty('___body', params):
            return self._e('PARAMS_NOT_EXIST')

        req_body = params['___body']
        if self.common_utils.is_empty('name', req_body):
            return self._e('PARAMS_NOT_EXIST')

        result = await self.model.modify({
            'name': req_body['name'],
            'admin_id': self.user_data['admin_id']
        })
        if not result:
            return self._e('EXECUTION_FAILED')

        return self._rs()

