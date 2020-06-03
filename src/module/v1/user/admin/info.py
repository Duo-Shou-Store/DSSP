# -*- coding:utf-8 -*-

"""
管理员信息
@author fuweiyi
@time 2020/6/2
"""
from base.base import Base


class Controller(Base):

    auth = (('admin', 'platform'), )

    async def get(self):
        """
        查询管理员列表或详细信息
        request body:
            {
                "admin_id": string 管理员ID.
                "search_key": string 搜索关键字，模糊搜索name/account
                "status": Int 状态, 1 正常，-1 冻结
                "page_index": Int 页码
                "page_size": Int 每页数量
            }

        return data:
            如果请求参数有admin_id，则返回指定administrator的详细信息。反之返回分页列表数据
            详细信息：
            {
                "admin_id": "",
                "account": "",
                "name": "",
                "status": "",
                "permission": [],
                "create_time": "",
                "last_update_time": ""
            }
            分页列表数据：
            {
                "list": [
                    {
                        "admin_id": "",
                        "account": "",
                        "name": "",
                        "status": "",
                        "create_time": "",
                        "last_update_time": ""
                    }
                ],
                "rows": 1
            }
        """
        params = self.params()
        params['admin_id'] = ''
        params['user_type'] = ''
        result = await self.do_service('user.admin.service', 'query', params)
        self.out(result)

    async def post(self):
        params = self.params()
        result = await self.do_service('user.admin.service', 'create', params)
        self.out(result)

    async def put(self):
        params = self.params()
        result = await self.do_service('user.admin.service', 'modify', params)
        self.out(result)

    async def delete(self):
        params = self.params()
        result = await self.do_service('user.admin.service', 'delete', params)
        self.out(result)
