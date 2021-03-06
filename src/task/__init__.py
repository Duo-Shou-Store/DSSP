# -*- coding: utf-8 -*-

"""
@author: Yuiitsu
@file: __init__.py
@time: 2018/6/5 10:59
"""
import json
import random

from tools.logs import logs as logger
from tools.date_json_encoder import CJsonEncoder
from tools.date_utils import DateUtils
from source.async_redis import AsyncRedis
from source.async_model import AsyncModelBase
from source.properties import properties
from .report import Report
import sys
import traceback

redis = AsyncRedis()
date_utils = DateUtils()

task_queue = properties.get('task', 'cache', 'task_queue')
failed_queue = properties.get('task', 'cache', 'failed_queue')
loop_num = int(properties.get('task', 'task', 'task_num'))
server_key = properties.get('task', 'cache', 'servers')
server_coroutine_key = properties.get('task', 'cache', 'server_coroutine')


async def save_to_db(data):
    # async def save_to_db(task_unique_id, service_path, method, params_json):
    """
    保存任务到DB
    :param data: list
        data[][task_unique_id]
        data[][service_path]
        data[][method]
        data[][params_json]
        data[][key1]
        data[][key2]
        data[][key3]
    :return:
    """
    if isinstance(data, dict):
        data = [data]

    model = AsyncModelBase()
    sql_list = []
    for item in data:
        key = 'task_unique_id, service_path, method, key1, key2, key3, params, create_time'
        val = '%s, %s, %s, %s, %s, %s, %s, %s'
        duplicate = [
            'params = %s',
            'create_time = %s'
        ]
        value = (
            item['task_unique_id'],
            item['service_path'],
            item['method'],
            item.get('key1', ''),
            item.get('key2', ''),
            item.get('key3', ''),
            item['params_json'],
            DateUtils.time_now(),
            item['params_json'],
            DateUtils.time_now()
        )
        sql_list.append({
            model.sql_constants.SQL_TYPE: model.sql_constants.INSERT,
            model.sql_constants.TABLE_NAME: 'tbl_cfg_task',
            model.sql_constants.DICT_DATA: {
                model.sql_constants.KEY: key,
                model.sql_constants.VAL: val,
                model.sql_constants.DUPLICATE_KEY_UPDATE: duplicate
            },
            model.sql_constants.VALUE_TUPLE: value
        })
    #
    result = await model.do_sqls(sql_list)
    if result is None:
        for item in data:
            logger.info('Task Add [%s] to DB failed, path [%s], method [%s], params: %s',
                        item['task_unique_id'], item['service_path'], item['method'], item['params_json'])
    else:
        for item in data:
            logger.info('Task Add [%s] to DB success, path [%s], method [%s], params: %s',
                    item['task_unique_id'], item['service_path'], item['method'], item['params_json'])

    return result


async def update_to_db(task_unique_id, status):
    """
    更新任务状态
    :param task_unique_id:
    :param status:
    :return:
    """
    model = AsyncModelBase()
    fields = [
        'status = %s',
        'execute_time = %s'
    ]
    condition = 'task_unique_id = %s'
    value = (status, DateUtils.time_now(), task_unique_id)
    result = await model.update('tbl_cfg_task', {
        model.sql_constants.FIELDS: fields,
        model.sql_constants.CONDITION: condition
    }, value)
    if result is None:
        logger.info('Task Update [%s] failed, status: %s',
                    task_unique_id, status)
    else:
        logger.info('Task Update [%s] to DB success, status: %s',
                    task_unique_id, status)

    return result


async def add(
        path='',
        method='',
        arguments=None,
        is_priority=False,
        sub_task=None,
        task_unique_id=None,
        batch_data=None):
    """
    添加任务
    :param path: 调用包文件路径
    :param method:  调用方法
    :param arguments: 请求参数
    :param is_priority: 是否优先处理(True or False)
    :param sub_task: 是否有子任务
            sub_task['queue_key'] 目标队列key
            sub_task['task_num'] 任务数
    :param task_unique_id
    :param batch_data: list
        batch_data[][service_path]
        batch_data[][method]
        batch_data[][arguments]
        batch_data[][key1]
        batch_data[][key2]
        batch_data[][key3]
    :return:
    """
    #
    arguments_json = json.dumps(arguments, cls=CJsonEncoder)
    if not task_unique_id:
        task_unique_id = str(int(DateUtils.timestamps_now())) + str(random.randrange(10000, 100000))

    logger.info('Task Add [%s], path [%s], method [%s], params: %s',
                task_unique_id, path, method, arguments_json)
    #
    if batch_data:
        for item in batch_data:
            if not item.get('task_unique_id'):
                item['task_unique_id'] = str(int(DateUtils.timestamps_now())) + str(random.randrange(10000, 100000))
            #
            item['params_json'] = json.dumps(item['arguments'], cls=CJsonEncoder)
            # del item['arguments']
    else:
        batch_data = [{
            'task_unique_id': task_unique_id,
            'service_path': path,
            'method': method,
            'params_json': arguments_json
        }]
    #
    await save_to_db(batch_data)
    for item in batch_data:
        params = {
            'task_unique_id': item['task_unique_id'],
            'path': item['service_path'],
            'method': item['method'],
            'key1': item.get('key1', ''),
            'key2': item.get('key2', ''),
            'key3': item.get('key3', ''),
            'arguments': item['arguments'],
            'sub_task': sub_task
        }

        try:
            params = json.dumps(params, cls=CJsonEncoder)
            if is_priority:
                result = await redis.rpush(task_queue, params)
            else:
                result = await redis.lpush(task_queue, params)
            #
            if result:
                logger.info('Task Add [%s] to QUEUE success, path [%s], method [%s], '
                            'key1 [%s], key2 [%s], key3 [%s], params: %s',
                            item['task_unique_id'], item['service_path'], item['method'],
                            item.get('key1', ''), item.get('key2', ''), item.get('key3', ''), item['params_json'])
            else:
                logger.info('Task Add [%s] to QUEUE failed, path [%s], method [%s], ',
                            'key1 [%s], key2 [%s], key3 [%s], params: %s',
                            item.get('key1', ''), item.get('key2', ''), item.get('key3', ''), item['params_json'])
        except Exception as e:
            await Report.report('添加任务异常', e)


async def get_one(task_queue_key=None):
    """
    从队列里获取一条数据
    :param task_queue_key:
    :return:
    """
    result = await redis.rpop(task_queue_key if task_queue_key else task_queue)
    return result


async def save_task_error(task, e):
    """
    保存失败任务信息
    :param task: 任务数据
    :param e: 异常信息
    :return:
    """
    try:
        task = json.loads(task) if isinstance(task, str) else task
        trace = ''.join(traceback.format_exception(*sys.exc_info())[-2:])
        task = json.dumps({
            'task': task,
            'e': trace,
            'time': date_utils.time_now()
        }, cls=CJsonEncoder)
        await redis.lpush(failed_queue, task)
    except Exception as e:
        logger.exception(e)
        raise


async def register_server(server_name, create_time):
    """
    注册服务
    :param server_name:
    :param create_time:
    :return:
    """
    logger.info('Task Server [%s] Registered, time: %s', server_name, str(create_time))
    result = await redis.hset(server_key, server_name, 1)
    if result is None:
        logger.info('Task Server [%s] Registered failed', server_name)
    else:
        logger.info('Task Server [%s] Registered success', server_name)

    return True


async def register_coroutine(server_name, num, create_time):
    """
    注册协程
    :param server_name:
    :param num:
    :param create_time:
    :return:
    """
    key = server_coroutine_key + ':' + server_name
    result = await redis.hset(key, num, create_time)
    return True


async def refresh_coroutine(server_name, num, refresh_time):
    """
    刷新协程
    :param server_name:
    :param num:
    :param refresh_time:
    :return:
    """
    key = server_coroutine_key + ':' + server_name
    result = await redis.hset(key, num, refresh_time)
    return True


async def get_server_status(server_name):
    """
    获取服务状态
    :param server_name:
    :return:
    """
    result = await redis.hget(server_key, server_name)
    if not result:
        result = '0'

    return result


if __name__ == '__main__':
    add('goods.stock.service', 'update_sales', {
        "goods_sales": [
            {
                "goods_id": "G009MV3GGO",
                "sku_id": "S00CBJOTHY",
                "sales": -1
            }
        ], "trigger_position": "return_sku_stock"
    })

