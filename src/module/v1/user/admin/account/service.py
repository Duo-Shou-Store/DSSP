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
            params['account']
            params['admin_id']
        :return:
        """
        if self.common_utils.is_empty('account', params) and self.common_utils.is_empty('admin_id', params):
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

    async def modify_password(self, params):
        """
        修改登录用户的密码
        @param params:
            params['old_password'] (*)
            params['password'] (*)
            params['confirm_password'] (*)
        @return:
        """
        if self.common_utils.is_empty('___body', params) \
                or self.common_utils.is_empty(['old_password', 'password', 'confirm_password'], params['___body']):
            return self._e('PARAMS_NOT_EXIST', message_ext='原密码，新密码和确认密码都不能为空')

        req_args = params['___body']
        old_password = req_args['old_password']
        password = req_args['password']
        confirm_password = req_args['confirm_password']
        # 检查密码是否符合要求
        if not self.common_utils.check_password_level(password):
            return self._e('PASSWORD_MISMATCH_RULES', message_ext='只能包含数字，大小字母，部分特殊符号')

        # 检查密码长度
        if len(password) < 6 or len(password) > 32:
            return self._e('PASSWORD_LENGTH_ERROR', message_ext='须在6 - 32个字符之间')

        # 检查新密码和确认密码是否一致
        if password != confirm_password:
            return self._e('CONFIRM_PASSWORD_NOT_MATCH')

        account_res = await self.query_one({
            'admin_id': self.user_data['admin_id']
        })
        if account_res['code'] != 0:
            return account_res

        account = account_res['data']
        # 检查原密码是否正确
        if self.common_utils.md5(self.common_utils.md5(old_password) + account['salt']) != account['password']:
            return self._e('OLD_PASSWORD_NOT_MATCH')

        salt = self.common_utils.salt(6)
        password = self.common_utils.md5(self.common_utils.md5(password) + salt)

        result = await self.model.modify_password({
            'admin_id': self.user_data['admin_id'],
            'password': password,
            'salt': salt
        })
        if result is None:
            return self._e('EXECUTION_FAILED')

        return self._rs()
