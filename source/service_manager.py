# -*- coding:utf-8 -*-

"""
@author: delu
@file: service_manager.py
@time: 17/4/18 下午5:21
service 服务模块
"""
import re
import importlib
import traceback

from tools.httputils import HttpUtils
from tools.logs import logs as logger
import time


class ServiceManager(object):

    @staticmethod
    def do_local_service(service_path, method, params=None, version=''):
        """
        执行本地服务
        :param service_path: 
        :param method: 
        :param params: 
        :param version: 
        :return: 
        """
        path_version = ServiceManager.get_loader_version(service_path)
        if path_version:
            model = importlib.import_module('src.module.' + service_path)
        else:
            model = importlib.import_module('src.module.' + version + '.' + service_path)

        service = model.Service()
        func = getattr(service, method)

        result = func(params)
        return result

    @staticmethod
    def do_remote_service(url, params, http_type='get'):
        """
        执行远程服务
        :param url: 
        :param params: 
        :return: 
        """
        pass

    @staticmethod
    def do_service(service_path='', method='', params=None, version='', power=None):
        """
        执行服务
        :param service_path: 
        :param method: 
        :param params: 
        :param version: 
        :return: 
        """
        # 判断该服务是否需要远程支持
        # if is_remote:
        #     url = REMOTE_CONTROLLER['host'] + REMOTE_CONTROLLER[service_path][method][0]
        #     return ServiceManager.do_remote_service(url, params, http_type=REMOTE_CONTROLLER[service_path][method][1])
        # else:
        return ServiceManager.do_local_service(service_path, method, params, version)

    @staticmethod
    def get_fun(service_path, method, params, version='v1'):
        """
        根据方法路径获取方法实例
        :param service_path:
        :param method:
        :param params:
        :param version:
        :return:
        """
        model = importlib.import_module(version + '.module.' + service_path)
        service = model.Service()

        # 如果语言不存在，则默认为中文
        if 'language' not in params or not params['language']:
            params['language'] = 'cn'
        language_module = importlib.import_module('language.' + params['language'])
        setattr(service, 'language_code', language_module.Code)
        func = getattr(service, method)
        return func

    @staticmethod
    def get_loader_version(path=None):
        """
        获取调用者的Version
        """
        version = None
        if path:
            version = re.findall(r"^v(.+?)\.", path)
            if version:
                version = 'v' + version[0]

        if not version:
            caller = traceback.extract_stack()[-3]
            caller_path = caller[0]
            version = re.findall(r"/src/module/(.+?)/", caller_path)
            if version:
                version = version[0]
        return version
