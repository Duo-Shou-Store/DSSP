# -*- coding:utf-8 -*-

"""
@author: onlyfu
@time: 2021/6/28
项目初始化
本程序会寻找项目内的MODEL类，并根据它们的参数创建或更新表结构
"""
import os
import sys
import importlib

parent_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(parent_path)
root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'module')
root_package = 'src.module'
sys.path.append(parent_path)
sys.path.append(root_path)


import asyncio
from source.service_manager import ServiceManager
from source.properties import properties
from tools.logs import logs as logger


class DBInit(object):

    sql_data = []
    sql_list = []

    async def init(self):
        self.get_db_structure()
        service = 'v1._table_init.service'
        version = ServiceManager.get_loader_version(service)
        result = await ServiceManager.do_service(service, 'execute', self.sql_data, version=version)

    def build_sql(self):
        """
        将从文件中获取的sql对象转换为sql字符串
        """
        for item in self.sql_data:
            print(item)

    def get_db_structure(self):
        """
        从项目文件中寻找名称为mode.py的文件，将获取它的_DB_INIT和_DB_UPDATE成员变量，将它们添加到sql_data里
        """
        dir_name = root_dir
        for parent, dir_names, file_names in os.walk(dir_name):
            for file_name in file_names:
                model_path = parent.replace(root_dir, '').replace('\\', '/') + '/' + file_name.replace('.py', '')
                model_key = root_package + model_path.replace('/', '.').replace('\\', '.')
                #
                if file_name.startswith('_tbl_'):
                    try:
                        module = importlib.import_module(model_key)
                        if hasattr(module, 'Table'):
                            Table = module.Table
                            for name, value in vars(Table()).items():
                                if name in ['_INIT_TABLE_STRUCTURE', '_INIT_TABLE_DATA', '_UPDATE_TABLE']:
                                    self.sql_data.append(value)
                                    print('%s=%s' % (name, value))
                    except Exception as e:
                        logger.info(model_key)
                        logger.exception(e)


def run():
    config_file = '../conf/'
    arguments = sys.argv
    for k, v in enumerate(arguments):
        if v == '-c':
            config_file = arguments[k + 1]

    # 加载配置文件
    properties.build(config_file)
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(DBInit().init())


if __name__ == '__main__':
    run()
