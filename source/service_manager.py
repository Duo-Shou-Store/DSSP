# -*- coding:utf-8 -*-

"""
@author: onlyfu
@time: 2020/6/2
"""
import re
import importlib
import traceback


class ServiceManager(object):

    @staticmethod
    def do_remote_service(url, params):
        """
        执行远程服务
        :param url: 
        :param params: 
        :return: 
        """
        pass

    @staticmethod
    def do_service(service_path='', method='', params=None, version='', power=None, user_data=None):
        """
        执行服务
        :param service_path: 
        :param method: 
        :param params: 
        :param version: 
        :param power:
        :param user_data:
        :return:
        """
        path_version = ServiceManager.get_loader_version(service_path)
        if path_version:
            model = importlib.import_module('src.module.' + service_path)
        else:
            model = importlib.import_module('src.module.' + version + '.' + service_path)

        service = model.Service()
        if user_data:
            service.user_data = user_data
        #
        func = getattr(service, method)

        result = func(params)
        return result

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
