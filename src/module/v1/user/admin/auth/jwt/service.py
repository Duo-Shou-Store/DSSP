# -*- coding:utf-8 -*-

"""
@package:
@file: service.py
@author: yuiitsu
@time: 2020-05-24 18:13
"""
from base.service import ServiceBase
from source.properties import properties
from tools.jwt import JWT
from .return_code import Code


class Service(ServiceBase):

    def __init__(self):
        self.return_code = Code

    async def get_access_token(self, params):
        """
        获取商户管理员的JWT ACCESS TOKEN
        :param params:
            params['account'] (*)
            params['password'] (*)
        :return:
            {
                access_token: 'JWT token',
                expires_in: 7200,
                refresh_expires_in: 2592000
            }
            access_token:
                admin_id:
                user_type: 用户类型
                exp: 过期时间
                refresh_expires_in: 刷新过期时间
                iat: 创建时间

        """
        if self.common_utils.is_empty('___body', params) \
                or self.common_utils.is_empty('account', params['___body']) \
                or self.common_utils.is_empty('password', params['___body']):
            return self._e('JWT_GET_PARAMS_ERROR')

        account = params['___body']['account']
        password = params['___body']['password']
        account_res = await self.cs('v1.user.admin.account.service', 'query_one', {
            'account': account
        })
        if account_res['code'] != 0:
            return self._e('ACCOUNT_OR_PASSWORD_ERROR')

        account_data = account_res['data']
        # 检查密码
        if self.common_utils.md5(self.common_utils.md5(password) + account_data['salt']) != account_data['password']:
            return self._e('ACCOUNT_OR_PASSWORD_ERROR')

        # 从配置文件中获取过期时间与刷新过期时间
        expires_in = int(properties.get('setting', 'jwt', 'expires_in'))
        refresh_expires_in = int(properties.get('setting', 'jwt', 'refresh_expires_in'))
        #
        access_token = JWT.encode({
            'admin_id': account_res['data']['admin_id'],
            'user_type': 'admin',
            'exp': expires_in,
            'iat': int(self.date_utils.timestamps_now()),
        })

        return self._rs({
            'access_token': access_token,
            'expires_in': expires_in,
            'refresh_expires_in': refresh_expires_in
        })
