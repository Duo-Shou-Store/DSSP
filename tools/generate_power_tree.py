# -*- coding:utf-8 -*-

"""
@author: conan
@time: 2018/3/21
"""
import re


class PowerTree:
    """
    定义权限的数据结构
    @author xhb
    @time 2017/12/06
    """

    def __init__(self, power_id):
        self.name = ''
        self.parent_id = 0
        self.power_id = power_id
        self.path = ''
        self.is_check_path = True
        self.index = 0
        self.group = 0
        self.children = []

    def get_dict(self):
        power_dict = {
            'parent_id': self.parent_id,
            'power_id': self.power_id,
            'name': self.name,
            'path': self.path,
            'is_check_path': self.is_check_path,
            'index': self.index,
            'group': self.group
        }

        children_list = []
        for child in self.children:
            children_list.append(child.get_dict())

        power_dict['child'] = children_list

        return power_dict


class GeneratePowerTree(object):
    """
    生成权限树
    """
    def __init__(self):
        self.temp_node = {}

    def generate_power_tree(self, tree):
        """
        生成权限树
        :param tree: __init__.py 中 所有node列表
        :return:
        """
        parent_id = 'root'
        power_id = 'root'
        name = ''
        path = ''
        is_check_path = True

        root = PowerTree(power_id)
        root.parent_id = parent_id
        root.name = name
        root.path = path
        root.is_check_path = is_check_path

        root_key = power_id
        power_dict = {root_key: root}

        for item in tree:
            parent_id = item['parent_id']
            power_id = item['power_id']
            name = item['name']
            path = item['path']
            is_check_path = item['is_check_path'] if 'is_check_path' in item else False
            index = item['index'] if 'index' in item else 0
            group = item['group'] if 'group' in item else 0

            power_node = PowerTree(power_id)
            power_node.parent_id = parent_id
            power_node.name = name
            power_node.path = path
            power_node.is_check_path = is_check_path
            power_node.index = index
            power_node.group = group

            # 根据node is_check_path 判断是否检查路径，True检查
            if is_check_path:
                # 如果parent_id不存在，或者子节点找上一级节点路径不匹配，过滤掉
                if parent_id in power_dict.keys():
                    parent_path = power_dict[parent_id].path
                    power_node_path = power_node.path
                    pattern = re.compile(parent_path)
                    if pattern.match(power_node_path) or parent_path == '':
                        # index 存在，按照index排序
                        if index:
                            self.sort_node(power_node, index, parent_id, power_dict)
                            power_dict[power_id] = power_node
                        else:
                            power_dict[parent_id].children.append(power_node)
                            power_dict[power_id] = power_node
                else:
                    self.sort_node(power_node, index, parent_id)
            else:
                if parent_id in power_dict.keys():
                    # index 存在，按照index排序
                    if index:
                        self.sort_node(power_node, index, parent_id, power_dict)
                        power_dict[power_id] = power_node
                    else:
                        power_dict[parent_id].children.append(power_node)
                        power_dict[power_id] = power_node
                else:
                    self.sort_node(power_node, index, parent_id)

        result_tree = power_dict[root_key].get_dict()
        result_power_tree = result_tree['child']
        return result_power_tree

    def sort_node(self, power_node, index, parent_id, *args):
        """
        1 判断args是否存在,存在对power_dict[parent_id].children排序，不存在对temp_node[parent_id]排序
        2 index 存在，按照index进行插入排序，不存在直接追加
        :param power_node: 权限节点
        :param index:      节点顺序索引
        :param parent_id:  父节点名称
        :param args:      可变参数(power_dict)
        :return: node_dict
        """
        # 判断是否传递power_dict
        if len(args) == 1:
            node_dict = args[0]
            if power_node.power_id in self.temp_node:
                power_node.children = self.temp_node[power_node.power_id]
            node_list = node_dict[parent_id].children
        else:
            node_dict = self.temp_node
            if parent_id not in node_dict:
                node_dict[parent_id] = []
            node_list = node_dict[parent_id]

        insert_node_index = -1
        for k, child in enumerate(node_list):
            child_index = child.index if hasattr(child, 'index') else 0
            if float(child_index) > float(index):
                insert_node_index = k
                break

        if insert_node_index == -1:
            node_list.append(power_node)
        else:
            node_list.insert(insert_node_index, power_node)
        return node_dict

# if __name__ == '__main__':
#     import json
#     from route import power
#     power_tree = GeneratePowerTree().generate_power_tree(power)
#     print json.dumps(power_tree)
