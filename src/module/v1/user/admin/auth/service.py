# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/8/30
"""
import tornado.gen
from base.service import ServiceBase


class Service(ServiceBase):

    user_model = None

    def __init__(self):
        self.user_model = self.import_model('user.model')

    @tornado.gen.coroutine
    def login(self, params):
        """
        @param params:
        @return:
        """
        if self.common_utils.is_empty(['account', 'password'], params):
            raise self._gre('PARAMS_NOT_EXIST')

    @tornado.gen.coroutine
    def quit(self, params):
        """
        退出登录
        :return:
        """
        if 'token' in params and params['token']:
            cache_key = self.cache_key_predix.ADMIN_TOKEN + self.md5(params['token'])
            yield self.redis.delete(cache_key)

        raise self._gre('SUCCESS')
