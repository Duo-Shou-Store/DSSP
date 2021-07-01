#!usr/bin/env python
# -*- coding:utf-8 -*-

import json
import time
import re
from tornado.web import Finish

from .return_code import Code
from source.controller import Controller
from source.service_manager import ServiceManager as serviceManager
from source.properties import properties
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
    user_data = {}

    async def prepare(self):
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
        if self.request.method in ('POST', 'PUT') and content_type != 'application/json':
            self.out(self._e('CONTENT_TYPE_ERROR'))

        # 检查访问服务是否需要授权校验
        if self.auth:
            if self.auth[0] is not None:
                await self.check_authorization_status(self.auth[0], self.auth[1])

    async def check_authorization_status(self, authorizations, no_check_control):
        """
        检查用户授权状态
        @param authorizations:
        @param no_check_control:
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

        # self._params['user_data'] = auth_data
        self.user_data = auth_data
        #
        if auth_data['user_type'] not in authorizations:
            self.out(self._e('AUTH_ERROR'))

        if auth_data['user_type'] == 'admin':
            await self.__check_power(auth_data, no_check_control)

    async def __check_power(self, user_data, no_check_control):
        """
        @param user_data:
        @param no_check_control:
        @return:
        """
        # 1 获取店铺权限
        # 2 group_id=0 超级管理员,查看用户请求power是否符合店铺权限
        # 3 group_id>0 普通管理员,查看用户请求power是否符合普通用户权限(shop_id)
        if not no_check_control:
            # 获取前端请求uri，替换api全段字段，用户请求权限
            base_url_prefix = properties.get('setting', 'base', 'BASE_URL_PREFIX') \
                .replace('BASE_URL_PREFIX=', '').replace('\n', '')
            power = self.request.uri.replace(base_url_prefix, '')
            if 'group_id' in user_data and int(user_data['group_id']) >= 0:
                auth_error_flag = True
                # 管理员menu(每个用户真正的权限树,不管是超级管理员，还是普通管理员)
                menu_params = {
                    'group_id': user_data['group_id'],
                }
                menu_result = await self.cs('v1.user.auth.menu.service', 'query_menu', menu_params)
                shop_power = self.get_path(menu_result['data'])
                # 检查请求url的power是否匹配用户权限树shop_power
                for power_tree in shop_power:
                    # 用shop_power 匹配 power
                    # shop_power: /user/auth/power
                    # power: /user/auth/power/query
                    pattern = re.compile(power_tree)
                    if pattern.match(power):
                        auth_error_flag = False
                        break

                # 检查权限
                if auth_error_flag:
                    self.out(self._e('AUTH_ERROR'))
            else:
                self.out(self._e('AUTH_ERROR'))

    def out(self, data):
        """
        @param data:
        @return:
        """
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_status(data['status'])
        del data['status']
        self.write(self.json.dumps(data, cls=CJsonEncoder))
        raise Finish()

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
        self.out(self._e('REQUEST_TYPE_ERROR'))

    async def post(self):
        """
        重写父类post方法，接受POST请求
        如果执行到此方法，说明请求类型错误
        """
        self.out(self._e('REQUEST_TYPE_ERROR'))

    async def put(self):
        """
        重写父类put方法，接受PUT请求
        如果执行到此方法，说明请求类型错误
        """
        self.out(self._e('REQUEST_TYPE_ERROR'))

    async def delete(self):
        """
        重写父类delete方法，接受DELETE请求
        如果执行到此方法，说明请求类型错误
        """
        self.out(self._e('REQUEST_TYPE_ERROR'))

    async def patch(self):
        """
        重写父类delete方法，接受DELETE请求
        如果执行到此方法，说明请求类型错误
        """
        self.out(self._e('REQUEST_TYPE_ERROR'))

    def cs(self, service_path, method, params):
        """
        调用服务
        :param service_path: 
        :param method: 
        :param params: 
        :return: 
        """
        version = serviceManager.get_loader_version(service_path)
        return serviceManager.do_service(
            service_path,
            method,
            params=params,
            version=version,
            user_data=self.user_data,
            context=self
        )

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

    def get_path(self, data, power_path_list=None):
        """
        1 遍历用户权限树，如果有child，获得child的path，如果没有，返回power['path']
        2 递归的遍历child获得path,直到所有child为空
        3 将所有path加载到power_tree 列表中
        4 获取子路径
        :param data: 用户权限树
        :return:
        """
        if power_path_list is None:
            power_path_list = []
        for power in data:
            power_path_list.append(str(power['path']))
            if power['child']:
                self.get_path(power['child'], power_path_list)
            # else:
            #     power_path_list.append(str(power['path']))
        return power_path_list

