# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2018/04/02
"""
import sys
import json
import tornado.ioloop

from src.conf.config import CONF
from tools.logs import logs
from tools.date_json_encoder import CJsonEncoder
from source.properties import properties
from source.service_manager import ServiceManager
from tools.common_util import CommonUtil


class Tester(object):

    path = ''
    method = ''
    params = {}
    logger = logs.logger

    async def main(self):
        version = CommonUtil.get_loader_version(self.path)
        try:
            result = await ServiceManager.do_service(self.path, self.method, self.params, version=version)
            print(json.dumps(result, cls=CJsonEncoder, ensure_ascii=False))
        except Exception as e:
            self.logger.exception(e)

    def run(self, func):
        config_file = ''
        arguments = sys.argv
        for k, v in enumerate(arguments):
            if v == '-c':
                config_file = arguments[k + 1]
        #
        config_file = config_file if config_file else CONF['tester']['properties_path']
        properties.build(config_file)
        #
        f = eval('self.' + func)
        f()
        #
        return tornado.ioloop.IOLoop.current().run_sync(self.main)


if __name__ == '__main__':
    tester = Tester()
    tornado.ioloop.IOLoop.current().run_sync(tester.main)
