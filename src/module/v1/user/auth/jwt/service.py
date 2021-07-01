# -*- coding:utf-8 -*-

"""
@author: 萎迷一心
@time: 2021/6/30
"""
from source.properties import properties
from base.service import ServiceBase
from .return_code import Code


class Service(ServiceBase):

    def __init__(self):
        self.return_code = Code

    async def get_access_token(self, params):
        """
        获取Access Token
        :param params:
            request_body: 请求数据体
                request_body['account'] (*)
                request_body['password'] (*)
                request_body['shop_id'] (*)
                request_body['user_type'] customer/admin, default to customer
        :return:
        """
        request_body = params['request_body']
        if not isinstance(request_body, dict):
            self._end('PARAMS_NOT_EXIST')

        if self.common_utils.is_empty(['account', 'password'], request_body):
            self._end('PARAMS_NOT_EXIST')

        user_type = request_body.get('user_type', 'customer')
        if user_type == 'customer':
            result = await self.customer_access_token(request_body)
        else:
            result = await self.admin_access_token(request_body)

        return result

    async def admin_access_token(self, params):
        """
        @param params:
        @return:
        """
        admin_result = await self.cs('user.admin.service', 'query_single_admin_full', params)
        admin = admin_result['data']
        if admin['status'] != 1:
            self._end('ACCOUNT_FREEZE')

        if self.md5(self.md5(params['password']) + admin['salt']) != admin['password']:
            return self._end('PASSWORD_ERROR')

        #
        iat = int(self.date_utils.timestamps_now())
        expires_in = int(properties.get('setting', 'jwt', 'expires_in'))
        exp = iat + expires_in
        result = {
            'exp': exp,
            'iat': iat,
            'user_type': 'admin',
            'group_id': admin['group_id'],
            'admin_id': admin['admin_id']
        }
        return self._rs(result)

    async def customer_access_token(self, params):
        pass
