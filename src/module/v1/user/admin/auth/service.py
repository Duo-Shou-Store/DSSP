# -*- coding:utf-8 -*-

"""
@package:
@file: service.py
@author: yuiitsu
@time: 2020-05-24 22:43
"""
from base.service import ServiceBase
from ..return_code import Code


class Service(ServiceBase):

    def __init__(self):
        self.return_code = Code

    async def register(self, params):
        """
        注册帐号
        :param params:
            params['account'] (*)
            params['password'] (*)
            params['confirm_password'] (*)
        :return:
        """
        if self.common_utils.is_empty(['account', 'password', 'confirm_password'], params):
            return self._e('PARAMS_NOT_EXIST', message='account, password, confirm_password不能为空')

        #
        if params['password'] != params['confirm_password']:
            return self._e('CONFIRM_PASSWORD_NOT_MATCH')

        # check the account
        account_res = await self.cs('v1.user.admin.account.service', 'query_one', {
            'account': params['account']
        })
        if account_res['code'] == 0:
            return self._e('DATA_EXIST', message='帐户已存在')

        # create the account
        result = await self.cs('v1.user.admin.account.service', 'create', {
            'account': params['account'],
            'password': params['password'],
            'account_type': 'email',
        })
        return result
