# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2018/04/02
"""
import os
import sys
import json
import time
import tornado.ioloop

from tools.logs import logs
from tools.date_json_encoder import CJsonEncoder
from source.properties import properties
from source.service_manager import ServiceManager


class Tester(object):

    path = ''
    method = ''
    params = {}
    result = None
    total_num = 0
    passed_num = 0
    callback = None
    test_status = 'passed'
    show_result = False
    logger = logs

    async def main(self):
        version = ServiceManager.get_loader_version(self.path)
        start_time = time.time()
        result = await ServiceManager.do_service(self.path, self.method, self.params, version=version)
        end_time = time.time()
        # 执行回调
        if self.callback:
            self.callback(result, end_time - start_time)

    def assert_equals(self, params, result):
        """
        检查给定值是否和结果值相同，包括list和dict
        @param params:
        @param result:
        @return:
        """
        self.test_status = 'passed'
        self.params = params
        self.total_num += 1

        #
        def callback(r, exec_time):
            if r == result:
                self.passed_num += 1
            else:
                self.test_status = 'failed'

            self.output(self.test_status, exec_time, r)
        #
        self.callback = callback
        #
        return tornado.ioloop.IOLoop.current().run_sync(self.main)

    def assert_in(self, params, key, val=None):
        """
        检查给定的key和val是否存在于结果中，存在pass，不存在fail
        @param params:
        @param key:
        @param val:
        @return:
        """
        self.test_status = 'passed'
        self.params = params
        self.total_num += 1

        #
        def callback(r, exec_time):
            if key in r:
                if val:
                    if r[key] == val:
                        self.passed_num += 1
                    else:
                        self.test_status = 'failed'
                else:
                    self.passed_num += 1
            else:
                self.test_status = 'failed'

            self.output(self.test_status, exec_time, r)

        #
        self.callback = callback
        #
        return tornado.ioloop.IOLoop.current().run_sync(self.main)

    def output(self, status, exec_time, result):
        color = '32'
        if status == 'failed':
            color = '31'
        #
        print('\033[1:{}m#{}: {}, {}ms\033[0m'
              .format(color, str(self.total_num), self.test_status, str(exec_time * 1000)))
        #
        if self.show_result:
            print('\033[1:{}m#{}, result: {}\033[0m'
                  .format(color, str(self.total_num), json.dumps(result, cls=CJsonEncoder, ensure_ascii=False)))

    def exec(self, params):
        """
        直接获取结果
        @param params:
        @return:
        """
        self.params = params

        def callback(r, exec_time):
            print('\033[1:32mresult: {}\033[0m'
                  .format(json.dumps(r, cls=CJsonEncoder, ensure_ascii=False)))
            print('\033[1:32mtime: {}ms\033[0m'.format(str(exec_time * 1000)))

        self.callback = callback
        return tornado.ioloop.IOLoop.current().run_sync(self.main)

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
        if self.total_num > 0:
            passed_rate = self.passed_num / self.total_num * 100
            print('Test result:')
            print('Total: {}, passed: {}, rate: {}%'
                  .format(str(self.total_num), str(self.passed_num), str(passed_rate)))


if __name__ == '__main__':
    tester = Tester()
    tornado.ioloop.IOLoop.current().run_sync(tester.main)
