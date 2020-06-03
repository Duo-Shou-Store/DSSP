# -*- coding:utf-8 -*-

import datetime
import hashlib
import importlib
import json
import time
from functools import wraps

import task
# from task import schedule
from constants.return_code import Code
from source.service_manager import ServiceManager as serviceManager
from tools.common_util import CommonUtil
from tools.date_utils import dateUtils
from tools.httputils import HttpUtils
from tools.logs import logs


class ServiceBase(object):
    time = time
    datetime = datetime
    json = json
    hashlib = hashlib
    return_code = Code
    http_utils = HttpUtils
    common_utils = CommonUtil
    date_utils = dateUtils
    logger = logs
    task = task

    def import_model(self, model_name):
        """
        加载数据类
        :param model_name: string 数据类名
        :return:
        """
        try:
            version = serviceManager.get_loader_version()
            model = importlib.import_module('src.module.' + version + '.' + model_name)
            return model.Model()
        except Exception as e:
            self.logger.exception(e)
            return None

    def do_service(self, service_path, method, params):
        """
        调用服务
        :param service_path: 
        :param method: 
        :param params:
        :return:
        """
        version = serviceManager.get_loader_version(service_path)
        return serviceManager.do_service(service_path, method, params=params, version=version)

    # async def load_extensions(self, trigger_position, data):
    #     """
    #     加载扩展程序
    #     :param trigger_position:
    #     :param data:
    #     :return:
    #     """
    #     data['trigger_position'] = trigger_position
    #     result = await self.do_service('v1.cfg.extensions.service', 'query', {'trigger_position': trigger_position})
    #     if result and 'code' in result and result['code'] == 0:
    #         # 发送消息
    #         for item in result['data']:
    #             service_path = item['package_path']
    #             method = item['method']
    #             await self.task.add(service_path, method, data)

    def _e(self, return_code_key, message='', message_ext='', data=''):
        """
        响应报文固定对象
        :param return_code_key:
        :param message:
        :param message_ext:
        :param data:
        :return:
        """
        result = self.return_code[return_code_key]
        if message:
            result['msg'] = message

        if message_ext:
            result['msg'] += ' ' + message_ext

        if data:
            result['data'] = data

        return result

    def _rs(self, data=None):
        """
        成功返回
        :param data: 
        :return: 
        """
        result = self._e('SUCCESS')
        if data:
            result['data'] = data
        return result

    @classmethod
    def params_set(cls, model=None, data=None):
        """
        数据对象设置
        :param model:
        :param data:
        :return:
        """
        def decorate(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                o = args[0]
                params = args[1]
                model_data = None
                if hasattr(o, model):
                    model_obj = getattr(o, model)
                    if hasattr(model_obj, data):
                        model_data = getattr(model_obj, data)

                new_args = args
                if model_data:
                    if isinstance(params, dict):
                        model_data.update(params)
                        new_args = (args[0], model_data)

                result = await func(*new_args, **kwargs)
                return result
            return wrapper
        return decorate
