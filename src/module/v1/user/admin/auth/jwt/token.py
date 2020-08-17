# -*- coding:utf-8 -*-

"""
获取商户管理员的Access Token API
@package:
@file: token.py
@author: yuiitsu
@time: 2020-05-24 18:14

request body:
    {
        account: 帐户名(*)
        password: 密码(*)
    }

return:
    {
        access_token: 'JWT token',
        expires_in: 7200,
        refresh_expires_in: 2592000
    }
"""
from base.base import Base


class Controller(Base):

    async def post(self):
        params = self.params()
        result = await self.cs('user.admin.auth.jwt.service', 'get_access_token', params)
        self.out(result)
