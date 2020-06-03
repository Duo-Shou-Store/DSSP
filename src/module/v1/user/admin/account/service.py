# -*- coding:utf-8 -*-

"""
@package:
@file: service.py
@author: yuiitsu
@time: 2020-05-24 18:39
"""
from base.service import ServiceBase
from .model import Model
from .return_code import Code


class Service(ServiceBase):

    def __init__(self):
        self.model = Model()
        self.return_code = Code

    async def query_one(self, params):
        """
        获取一条帐号记录
        :param params:
            params['account'] (*)
        :return:
        """
        if self.common_utils.is_empty(['account'], params):
            return self._e('PARAMS_NOT_EXIST', message_ext='account不能为空')

        data = await self.model.query_one(params)
        if not data:
            return self._e('DATA_NOT_EXIST')

        return self._rs(data)

    @ServiceBase.params_set('model', 'save_obj')
    async def create(self, params):
        """
        创建帐号，同时创建管理员信息
        :param params:
            params['account_type'] (*)
            params['account'] (*)
            params['password'] (*)
        :return:
        """
        if self.common_utils.is_empty(['account', 'account_type', 'password'], params):
            return self._e('PARAMS_NOT_EXIST')

        salt = self.common_utils.salt()
        password = self.common_utils.md5(self.common_utils.md5(params['password']) + salt)
        #
        admin_id = self.common_utils.create_uuid()
        result = await self.model.create({
            'admin_id': admin_id,
            'account': params['account'],
            'account_type': params['account_type'],
            'password': password,
            'salt': salt,
            'create_time': params['create_time']
        })
        if result is None:
            return self._e('CREATE_ACCOUNT_FAILED')

        return self._rs({
            'admin_id': admin_id
        })
