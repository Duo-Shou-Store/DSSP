# -*- coding:utf-8 -*-

"""
@author fuweiyi
@time 2021/6/30
"""
from tools.date_utils import DateUtils


class Table(object):

    table_name = 'tbl_um_admin_info'

    def __init__(self):
        self._INIT_TABLE_STRUCTURE = [
            """
            CREATE TABLE `{table_name}`  (
                `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '自增id',
                `admin_id` char(16) NOT NULL,
                `name` varchar(40) NOT NULL,
                `group_id` int(0) NOT NULL DEFAULT 0 COMMENT '分组ID',
                `mobile_number` varchar(20) NOT NULL DEFAULT '',
                `status` tinyint(0) NOT NULL DEFAULT 1 COMMENT '管理员状态，1为正常，0为禁用',
                `create_time` datetime NOT NULL,
                `last_update_time` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`),
                UNIQUE INDEX `name_idx`(`name`) USING BTREE
            );
            """.format(table_name=self.table_name)
        ]

        self._INIT_TABLE_DATA = [
            """
            INSERT INTO `{table_name}` 
            (admin_id, name, group_id, create_time, last_update_time) 
            VALUES 
            ('{admin_id}', '{name}', '{group_id}', '{create_time}', '{last_update_time}');
            """.format(
                table_name=self.table_name,
                admin_id='1',
                name='admin',
                group_id=0,
                create_time=DateUtils.time_now(),
                last_update_time=DateUtils.time_now()
            )
        ]

        self._UPDATE_TABLE = []

    @staticmethod
    def get_object():
        return {
            'admin_id': '',
            'name': '',
            'group_id': '',
            'mobile_number': '',
            'status': '',
            'create_time': DateUtils.time_now(),
            'last_update_time': DateUtils.time_now()
        }
