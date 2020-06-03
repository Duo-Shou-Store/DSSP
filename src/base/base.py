#!usr/bin/env python
# -*- coding:utf-8 -*-

import json
import time

from constants.return_code import Code
from source.controller import Controller
from source.service_manager import ServiceManager as serviceManager
from tools.date_json_encoder import CJsonEncoder
from tools.logs import logs
from tools.jwt import JWT


class Base(Controller):

    json = json
    time = time
    return_code = Code
    logger = logs
    _params = {}
    auth = None

    def prepare(self):
        """
        接受请求前置方法
            1.解析域名
            2.检查IP限制
            3.权限检查
        :return:
        """
        self._params = self.get_params()
        headers = self.request.headers
        content_type = headers['Content-Type']
        # 检查content type，必须使用application/json
        if content_type != 'application/json':
            self.out(self._e('CONTENT_TYPE_ERROR'))
            self.finish()

        # 检查访问服务是否需要授权校验
        if self.auth:
            if self.auth[0] is not None:
                self.check_authorization_status(self.auth[0])

    def check_authorization_status(self, authorizations):
        """
        检查用户授权状态
        @param authorizations:
        @return:
        """
        access_token = ''
        if self.request.headers.get('access_token'):
            access_token = self.request.headers['access_token']
        elif self.request.headers.get('Authorization'):
            access_token = self.request.headers['Authorization']
            access_token = access_token.split(' ')[1]

        auth_data = JWT.verify(access_token)
        if not auth_data:
            self.out(self._e('NOT_LOGGED_IN'))

        #
        if auth_data['user_type'] not in authorizations:
            self.out(self._e('PERMISSION_FORBIDDEN'))

        self._params.update(auth_data)

    def out(self, data):
        """ 
        输出结果
        :param data: 返回数据字典
        """
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(self.json.dumps(data, cls=CJsonEncoder))
        self.finish()

    def error_out(self, error, data='', status_code=500):
        """
        错误输出
        :param error: 错误信息对象
        :param data: 返回数据字典
        :param status_code: http status code, default 500
        :return:
        """
        out = error
        if data:
            out['data'] = data

        self.set_status(status_code)
        self.write(out)

    async def get(self):
        """
        重写父类get方法，接受GET请求
        如果执行到此方法，说明请求类型错误
        """
        self.error_out(self._e('REQUEST_TYPE_ERROR'), status_code=405)

    async def post(self):
        """
        重写父类post方法，接受POST请求
        如果执行到此方法，说明请求类型错误
        """
        self.error_out(self._e('REQUEST_TYPE_ERROR'), status_code=405)

    async def put(self):
        """
        重写父类put方法，接受PUT请求
        如果执行到此方法，说明请求类型错误
        """
        self.error_out(self._e('REQUEST_TYPE_ERROR'), status_code=405)

    async def delete(self):
        """
        重写父类delete方法，接受DELETE请求
        如果执行到此方法，说明请求类型错误
        """
        self.error_out(self._e('REQUEST_TYPE_ERROR'), status_code=405)

    async def patch(self):
        """
        重写父类delete方法，接受DELETE请求
        如果执行到此方法，说明请求类型错误
        """
        self.error_out(self._e('REQUEST_TYPE_ERROR'), status_code=405)

    def do_service(self, service_path, method, params):
        """
        调用服务
        :param service_path: 
        :param method: 
        :param params: 
        :return: 
        """
        version = serviceManager.get_loader_version(service_path)
        power_tree = self.settings['power_tree']
        return serviceManager.do_service(service_path, method, params=params, version=version,
                                         power=power_tree)

    def _e(self, return_code_key, message_ext='', data=''):
        """
        响应报文固定对象
        :param return_code_key:
        :param message_ext:
        :param data:
        :return:
        """
        result = self.return_code[return_code_key]
        if message_ext:
            result['msg'] += ' ' + message_ext

        if data:
            result['data'] = data

        return result

    def params(self, key=''):
        """
        获取参数中指定key的数据
        :param key:
        :return:
        """
        if self.request.body:
            try:
                ___body = self.request.body.decode(encoding='utf-8', errors='strict')
                self._params['___body'] = json.loads(___body)
            except Exception as e:
                self.logger.exception(e)

        if not key:
            return self._params
        elif key not in self._params:
            return ''
        else:
            return self._params[key]

    def get_user_agent(self):
        """
        获取用户访问数据
        :return:
        """
        request = self.request
        if 'Remote_ip' in request.headers and request.headers['Remote_ip']:
            ip = request.headers['Remote_ip']
        elif 'X-Forward-For' in request.headers and request.headers['X-Forward-For']:
            ip = request.headers['X-Forward-For']
        else:
            ip = request.remote_ip

        cookies = ''
        if request.cookies:
            for k, v in request.cookies.items():
                cookies += k + '=' + v.value + ';'

        try:
            user_agent = request.headers['User-Agent']
        except Exception as e:
            user_agent = ''

        return {
            'remote_ip': ip,
            'user_agent': user_agent,
            'cookies': cookies
        }
