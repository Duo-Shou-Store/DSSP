# -*- coding:utf-8 -*-

"""
@author: 萎迷一心
@time: 2021/6/30
"""
import tornado.gen
from base.base import Base
from tools.jwt import JWT

"""
获取JWT Access Token API
request body:
    {
        username: 帐户名(*)
        password: 密码(*)
        user_type: 类型，customer/admin，不传默认为customer
    }

return:
    {
        access_token: 'JWT token',
        expires_in: 7200,
    }
"""


class Controller(Base):

    async def post(self):
        params = self.params()
        result = await self.cs('user.auth.jwt.service', 'get_access_token', params)
        if result['code'] != 0:
            self.out(result)
            return

        encoded = JWT.encode(result['data'])
        result['data'] = {
            'access_token': encoded,
            'expires_in': result['data']['exp']
        }
        self.out(result)
