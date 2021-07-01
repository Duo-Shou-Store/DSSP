# -*- coding:utf-8 -*-

"""
@author: 萎迷一心
@time: 2021/6/29
"""
import tornado.gen
from base.base import Base


class Controller(Base):

    auth = (None, True)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        result = yield self.do_service('user.admin.auth.service', 'login', params)
        self.out(result)
