# -*- coding:utf-8 -*-

"""
@author fuweiyi
@time 2021/6/30
"""
from tools.date_utils import DateUtils


class Table(object):

    table_name = 'tbl_um_admin_account'

    def __init__(self):
        self._INIT_TABLE_STRUCTURE = [
            """
            CREATE TABLE `{table_name}`  (
                `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '自增id',
                `admin_id` char(16) NOT NULL,
                `account` varchar(50) NOT NULL,
                `password` char(32) NOT NULL DEFAULT '',
                `salt` char(6) NOT NULL,
                `account_type` varchar(20) NOT NULL DEFAULT '',
                `create_time` datetime NOT NULL,
                `last_update_time` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`),
                UNIQUE INDEX `account_idx`(`account`) USING BTREE,
                INDEX `admin_id_idx` (`admin_id`) USING BTREE 
            );
            """.format(table_name=self.table_name)
        ]

        self._INIT_TABLE_DATA = [
            """
            INSERT INTO `{table_name}` 
            (admin_id, account, password, salt, account_type, create_time, last_update_time) 
            VALUES 
            ('{admin_id}', '{account}', '{password}', '{salt}', '{account_type}', '{create_time}', '{last_update_time}');
            """.format(
                table_name=self.table_name,
                admin_id='1',
                account='admin',
                password='db7991b2cbef5d2989fff3410cc8b6a8',
                salt='kF9hjM',
                account_type='normal',
                create_time=DateUtils.time_now(),
                last_update_time=DateUtils.time_now()
            )
        ]

        self._UPDATE_TABLE = []

    @staticmethod
    def get_object():
        return {
            'admin_id': '',
            'account': '',
            'password': '',
            'salt': '',
            'account_type': '',
            'create_time': DateUtils.time_now(),
            'last_update_time': DateUtils.time_now()
        }
