# -*- coding:utf-8 -*-

"""
@author fuweiyi
@time 2020/6/11
"""
from base.service import ServiceBase
from .model import Model


class Service(ServiceBase):

    def __init__(self):
        self.model = Model()

    async def query_info(self, params):
        """
        获取指定店铺信息
        @param params:
            params['shop_id'] (*)
        @return:
        """
        if self.common_utils.is_empty('shop_id', params):
            raise self._e('PARAMS_NOT_EXIST')
