# -*- coding:utf-8 -*-
"""
配置文件属性
"""
import os
import re
import json
from tools.logs import logs


class Properties(object):

    properties = None
    path = ''
    data = {}
    logger = logs.logger

    def build(self, path):
        try:
            files = os.listdir(path)
        except Exception as e:
            self.logger.error(e)
            return False

        #
        for file in files:
            if not os.path.isdir(file) and file.endswith('.conf'):
                #
                filename = file.split('.')[0]
                self.data[filename] = {}
                section = ''
                #
                f = open(path + '/' + file, encoding='utf-8')
                lines = iter(f)
                for line in lines:
                    # 跳过注释行
                    if line.startswith('#'):
                        continue
                    # 检查是否section行
                    c = re.match("^\[(.+?)\]", line)
                    if c:
                        cs = c.groups()
                        section = cs[0]
                        self.data[filename][section] = {}
                    else:
                        # 检查是否option行
                        options = line.split('=')
                        if len(options) >= 2:
                            option = options[0]
                            value = ''.join(options[1:]).replace('\n', '')
                            self.data[filename][section][option] = value

    def get_all(self):
        return self.data

    def get(self, filename, section, option):
        try:
            return self.data[filename][section][option]
        except Exception as e:
            logs.exception(e)
            return ""


properties = Properties()


if __name__ == '__main__':
    properties.build('/Users/fuweiyi/code/apps/conf/duoshou')
