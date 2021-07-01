# -*- coding:utf-8 -*-

"""
@author: 萎迷一心
@time: 2021/6/30
"""
import tornado.gen
from base.base import Base


class Controller(Base):

    auth = (('admin', ), True)

    @tornado.gen.coroutine
    def get(self):
        params = self.params()
        params['admin_id'] = self.user_data['admin_id']
        res = yield self.cs('user.admin.service', 'query_single_admin_info', params)
        self.out(res)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        params['admin_id'] = self.user_data['admin_id']
        res = yield self.do_service('user.admin.service', 'create_admin', params)
        self.out(res)

    @tornado.gen.coroutine
    def put(self):
        params = self.params()
        params['admin_id'] = self.user_data['admin_id']
        res = yield self.do_service('user.admin.service', 'modify_info', params)
        self.out(res)

    @tornado.gen.coroutine
    def delete(self):
        params = self.params()
        params['admin_id'] = self.user_data['admin_id']
        res = yield self.do_service('user.admin.service', 'delete_info', params)
        self.out(res)
