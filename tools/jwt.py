# -*- coding:utf-8 -*-

"""
@package:
@file: jwt.py
@author: yuiitsu
@time: 2020-05-24 18:19
"""
import hashlib
import hmac
import base64
import json
from source.properties import properties
from tools.logs import logs as logger
from tools.date_utils import DateUtils as dateUtils


class JWT(object):

    @staticmethod
    def encode(data):
        """
        JWT签名
        :param data:
        :return:
        """
        header = {
            "typ": "JWT",
            "alg": "HS256"
        }
        header = json.dumps(header, separators=(',', ':')).encode('utf-8')
        header = base64.urlsafe_b64encode(header).replace(b'=', b'')

        p = json.dumps(data, separators=(',', ':')).encode('utf-8')
        p = base64.urlsafe_b64encode(p).replace(b'=', b'')
        secret_key = properties.get('setting', 'jwt', 'secret_key').encode('utf-8')
        content = header + b'.' + p

        signature = hmac.new(secret_key, content, digestmod=hashlib.sha256).digest()
        signature = base64.urlsafe_b64encode(signature).replace(b'=', b'')

        s = header + b'.' + p + b'.' + signature
        return s.decode('utf-8')

    @staticmethod
    def verify(access_token):
        """
        JWT验签
        :param access_token:
        :return:
        """
        if access_token:
            try:
                header, p, signature = access_token.split('.')
                p = p + '=' * (-len(p) % 4)
                p = base64.decodebytes(p.encode('utf-8')).decode('utf-8')
                p_dict = json.loads(p)
            except Exception as e:
                logger.exception(e)
                return False

            create_time = p_dict['iat']
            expires_in = p_dict['exp']
            time_now = int(dateUtils.timestamps_now())
            if create_time + expires_in < time_now:
                return False

            encoded = JWT.encode(p_dict)
            if encoded != access_token:
                return False

            return p_dict

        return False
