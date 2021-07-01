# -*- coding:utf-8 -*-

"""
@author: onlyfu
@time: 20/4/17
"""

Code = {
    'SUCCESS': {'status': 200, 'code': 0, 'msg': '成功'},
    'REQUEST_TYPE_ERROR': {'status': 405, 'code': 1001, 'msg': '请求类型错误'},
    'SQL_EXECUTE_ERROR': {'status': 500, 'code': 1002, 'msg': '数据库执行失败'},
    'CACHE_EXECUTE_ERROR': {'status': 500, 'code': 1003, 'msg': '缓存执行失败'},
    'PARAMS_NOT_EXIST': {'status': 400, 'code': 1004, 'msg': '参数错误'},
    'PARAMS_TYPE_ERROR': {'status': 400, 'code': 1005, 'msg': '参数类型错误'},
    'AUTH_ERROR': {'status': 403, 'code': 1006, 'msg': '用户无权限'},
    'NOT_LOGIN': {'status': 401, 'code': 1007, 'msg': '用户未登录'},
    'DATA_EXIST': {'status': 200, 'code': 1008, 'msg': '数据已存在'},
    'DATA_NOT_EXIST': {'status': 200, 'code': 1009, 'msg': '数据不存在'},
    'JSON_DATA_FORMAT_ERROR': {'status': 400, 'code': 1011, 'msg': 'JSON数据格式错误'},
    'SIGN_VERIFY_FAILED': {'status': 400, 'code': 1016, 'msg': '验签失败'},
    'HTTP_REQUEST_FAILED': {'status': 400, 'code': 1017, 'msg': 'HTTP请求失败'},
    'METHOD_NOT_EXIST': {'status': 400, 'code': 1018, 'msg': '方法未找到'},
    'NOT_AUTHORIZATION': {'status': 401, 'code': 1019, 'msg': '未授权'},
}
