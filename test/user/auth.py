# -*- coding:utf-8 -*-

"""
@package:
@file: auth.py
@author: yuiitsu
@time: 2020-05-24 23:14
"""
import os
from test.tester import Tester


class T(Tester):

    def register(self):
        self.path = 'v1.user.admin.auth.service'
        self.method = 'register'
        self.params = {
            'account': 'fuwy@foxmail.com',
            'password': '123456',
            'confirm_password': '123456'
        }

    def get_access_token(self):
        self.path = 'v1.user.admin.auth.jwt.service'
        self.method = 'get_access_token'
        self.params = {
            '___body': {
                'account': 'fuwy@foxmail.com',
                'password': '1234567'
            }
        }


if __name__ == '__main__':
    t = T()
    # t.run('register')
    t.run('get_access_token')
