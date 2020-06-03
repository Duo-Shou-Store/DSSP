# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2018/04/02
"""
import os
import sys
import json
import tornado.ioloop

from tools.logs import logs
from tools.date_json_encoder import CJsonEncoder
from source.properties import properties
from source.service_manager import ServiceManager


class Tester(object):

    path = ''
    method = ''
    params = {}
    logger = logs

    async def main(self):
        version = ServiceManager.get_loader_version(self.path)
        result = await ServiceManager.do_service(self.path, self.method, self.params, version=version)
        print(json.dumps(result, cls=CJsonEncoder, ensure_ascii=False))

    def run(self, func):
        path = os.getcwd().split('test')[-1]
        path_length = len(path.split('/'))
        file_relative_path = []
        for i in range(path_length):
            file_relative_path.append('../')

        config_file = ''.join(file_relative_path) + 'conf/'
        arguments = sys.argv
        for k, v in enumerate(arguments):
            if v == '-c':
                config_file = arguments[k + 1]
        #
        properties.build(config_file)
        #
        f = eval('self.' + func)
        f()
        #
        return tornado.ioloop.IOLoop.current().run_sync(self.main)


if __name__ == '__main__':
    tester = Tester()
    tornado.ioloop.IOLoop.current().run_sync(tester.main)
