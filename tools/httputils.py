# -*- coding:utf-8 -*-

"""
@author: delu
@file: httputils.py
@time: 17/5/2 上午10:36
"""
import urllib
import urllib.request
import urllib.parse
import json
import tornado.gen
from tornado.httpclient import HTTPRequest
from tornado.httpclient import AsyncHTTPClient
from tools.logs import logs

logger = logs


class HttpUtils(object):

    @staticmethod
    async def get(url, params=None, headers=None, is_json=False):
        if params:
            url = url + '?' + urllib.parse.urlencode(params)
        # if len(params) > 0:
        #     for key in params:
        #         # 字符串(中文)进行encode
        #         url_params += '%s=%s&' % (key, params[key])
        #     # 删除最后的&
        #     url = (url + url_params)[:-1]

        http_request = HTTPRequest(url, 'GET', headers=headers, validate_cert=False)
        http_client = AsyncHTTPClient()
        return_data = None
        try:
            fetch_result = await http_client.fetch(http_request)
            return_data = fetch_result.body
        except Exception as e:
            logger.info("HTTP GET RESULT: %s",  return_data)
            logger.exception(e)
            raise e
        final_result = HttpUtils.able_decode(return_data)
        if final_result:
            return_data = final_result

        if is_json and final_result:
            try:
                return_data = json.loads(return_data.replace('\r\n', ''))
            except Exception as e:
                logger.exception('json error', e)

        return return_data

    @staticmethod
    async def get_status(url, params=None, headers=None, is_json=False):
        if params:
            url = url + '?' + urllib.parse.urlencode(params)
        # if len(params) > 0:
        #     for key in params:
        #         # 字符串(中文)进行encode
        #         url_params += '%s=%s&' % (key, params[key])
        #     # 删除最后的&
        #     url = (url + url_params)[:-1]

        http_request = HTTPRequest(url, 'GET', headers=headers, validate_cert=False)
        http_client = AsyncHTTPClient()
        try:
            fetch_result = await http_client.fetch(http_request)
        except Exception as e:
            logger.exception(e)
            raise e

        return fetch_result

    @staticmethod
    async def post(url, params=None, headers=None, is_json=False, need_log=True, request_type='POST', auth_username='', auth_password='', need_cookie=False):
        logger.info('url: %s, params: %s', url, params)
        body = params if isinstance(params, str) else urllib.parse.urlencode(params)
        if request_type != 'POST':
            body = None
        http_request = HTTPRequest(url, request_type, body=body, headers=headers, validate_cert=False, auth_username=auth_username, auth_password=auth_password)
        http_client = AsyncHTTPClient()
        return_data = None
        response_headers = None
        try:
            fetch_result = await http_client.fetch(http_request)
            if need_cookie:
                response_headers = fetch_result.headers

            return_data = fetch_result.body
        except Exception as e:
            logger.info("HTTP POST RESULT: %s",  return_data)
            logger.exception(e)
            raise e
        final_result = HttpUtils.able_decode(return_data)
        if final_result:
            return_data = final_result

        if is_json and final_result:
            try:
                return_data = json.loads(return_data.replace('\r\n', ''))

                if need_cookie:
                    return_data['response_headers'] = response_headers
            except Exception as e:
                logger.exception('json error', e)
        if need_log:
            logger.info('response: %s', return_data)

        return return_data

    @staticmethod
    async def post_status(url, params=None, headers=None, is_json=False, need_log=True, request_type='POST',
                    auth_username='', auth_password=''):
        logger.info('url: %s, params: %s', url, params)
        body = params if isinstance(params, str) else urllib.parse.urlencode(params)
        if request_type != 'POST':
            body = None

        http_request = HTTPRequest(url, request_type, body=body, headers=headers, validate_cert=False,
                                   auth_username=auth_username, auth_password=auth_password)
        http_client = AsyncHTTPClient()
        try:
            fetch_result = await http_client.fetch(http_request)
            return_data = fetch_result.body
        except Exception as e:
            logger.exception(e)
            raise e

        if need_log:
            logger.info('response: %s', return_data)

        return fetch_result

    @staticmethod
    async def post_with_cert(url, params=None, headers=None, client_key=None, client_cert=None):
        body = params if isinstance(params, str) else urllib.parse.urlencode(params)
        http_request = HTTPRequest(url, 'POST', body=body, headers=headers, validate_cert=False, client_key=client_key,
                                   client_cert=client_cert)
        http_client = AsyncHTTPClient()
        fetch_result = await http_client.fetch(http_request)
        return fetch_result.body

    @staticmethod
    def able_decode(bytes_str):
        """
        判断bytes_str能否被utf-8编码
        :param bytes_str: 
        :return: 
        """
        try:
            if isinstance(bytes_str, bytes):
                return bytes_str.decode('utf-8')
            else:
                return False
        except Exception as e:
            return False


if __name__ == '__main__':
    # from tornado.ioloop import IOLoop
    #
    # def handle_response(response):
    #     if response.error:
    #         print("Error: %s" % response.error)
    #     else:
    #         print(response.body)
    #
    #
    # http_client = AsyncHTTPClient()
    # http_client.fetch("http://www.google.com/", handle_response)
    # IOLoop.current().start()

    import requests
    url = 'http://www.google.com'
    res = requests.get(url)
    print(res.text)
