# -*- coding:utf-8 -*-

"""
@author: onlyfu
@time: 2020/6/2
"""
import urllib
import urllib.request
import urllib.parse
import json
from tornado.httpclient import HTTPRequest
from tornado.httpclient import AsyncHTTPClient
from tools.logs import logs

AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient', max_clients=1000)
logger = logs


class HttpUtils(object):

    @staticmethod
    async def get(url, params=None, headers=None, is_json=False):
        """
        GET REQUEST
        @param url:
        @param params:
        @param headers:
        @param is_json:
        @return:
        """
        if params:
            url = url + '?' + urllib.parse.urlencode(params)

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

        http_request = HTTPRequest(url, 'GET', headers=headers, validate_cert=False)
        http_client = AsyncHTTPClient()
        try:
            fetch_result = await http_client.fetch(http_request)
        except Exception as e:
            logger.exception(e)
            raise e

        return fetch_result

    @staticmethod
    async def post(url, params=None, headers=None, is_json=False, auth_username='', auth_password=''):
        logger.info('url: %s, params: %s', url, params)
        body = params if isinstance(params, str) else urllib.parse.urlencode(params)
        http_request = HTTPRequest(
            url=url,
            method='POST',
            body=body,
            headers=headers,
            validate_cert=False,
            auth_username=auth_username,
            auth_password=auth_password
        )
        http_client = AsyncHTTPClient()
        return_data = None
        try:
            fetch_result = await http_client.fetch(http_request)
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
            except Exception as e:
                logger.exception('json error', e)

        return return_data

    @staticmethod
    async def post_status(url, params=None, headers=None, auth_username='', auth_password=''):
        logger.info('url: %s, params: %s', url, params)
        body = params if isinstance(params, str) else urllib.parse.urlencode(params)
        http_request = HTTPRequest(
            url=url,
            method='POST',
            body=body,
            headers=headers,
            validate_cert=False,
            auth_username=auth_username,
            auth_password=auth_password
        )
        http_client = AsyncHTTPClient()
        try:
            fetch_result = await http_client.fetch(http_request)
        except Exception as e:
            logger.exception(e)
            raise e

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
