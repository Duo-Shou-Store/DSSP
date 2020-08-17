# -*- coding:utf-8 -*-

"""
@author fuweiyi
@time 2020/6/4
"""
from base.base import Base


class Controller(Base):

    auth = (('admin', 'platform'), )

    async def put(self):
        """
        修改登录用户密码
        @return:
        """
        params = self.params()
        result = await self.cs('user.admin.account.service', 'modify_password', params)
        self.out(result)
