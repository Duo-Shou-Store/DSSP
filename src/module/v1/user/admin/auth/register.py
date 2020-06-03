# -*- coding:utf-8 -*-

"""
API 帐号注册
@package:
@file: register.py
@author: yuiitsu
@time: 2020-05-24 22:42


request body:
    {
        "account": "帐户名(*)"
        "password": "密码(*)"
        "confirm_password": "确认密码(*)"
    }

return:
    {
        "code": 0,
        'msg": "创建成功",
        "data": {
            "admin_id": "帐号ID"
        }
    }
"""
from base.base import Base


class Controller(Base):

    async def post(self):
        params = self.params()
        result = yield self.do_service('user.admin.auth.service', 'register', params)
        self.out(result)
