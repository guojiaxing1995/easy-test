# var_dick  变量字典 , data  被处理的数据, target_key 要找的目标key, new_key 赋值的新key, true_key  真实key,用来判断和目标key是否相等
import re
from flask import current_app


def deal_default(var_dick, data, target_key=None, new_key=None, true_key=None):
    if type(data) == list:
        for i in data:
            deal_default(var_dick, i, target_key, new_key)
    if type(data) == dict:
        for key, value in data.items():
            if type(value) == bool or type(value) == int or type(value) == str:
                deal_default(var_dick, value, target_key, new_key, key)
            if type(value) == dict:
                deal_default(var_dick, value, target_key, new_key)
            if type(value) == list:
                for i in value:
                    deal_default(var_dick, i, target_key, new_key)
    if type(data) == str:
        if target_key:
            if target_key == true_key:
                if new_key:
                    var_dick[new_key] = data
                else:
                    var_dick[true_key] = data
        else:
            var_dick[true_key] = data
    if type(data) == int:
        if target_key:
            if target_key == true_key:
                if new_key:
                    var_dick[new_key] = data
                else:
                    var_dick[true_key] = data
        else:
            var_dick[true_key] = data
    if type(data) is None:
        if target_key:
            if target_key == true_key:
                if new_key:
                    var_dick[new_key] = data
                else:
                    var_dick[true_key] = data
        else:
            var_dick[true_key] = data
    if type(data) == bool:
        if target_key:
            if target_key == true_key:
                if new_key:
                    var_dick[new_key] = data
                else:
                    var_dick[true_key] = data
        else:
            var_dick[true_key] = data

    return var_dick


# 获取目标value
def get_target_value(data, target_key):
    target_value = None
    if type(data) == list:
        for i in data:
            get_target_value(i, target_key)
    if type(data) == dict:
        for key, value in data.items():
            if key == target_key:
                if type(value) == str:
                    target_value = value
                if type(value) == int:
                    target_value = str(value)
                if type(value) == bool:
                    target_value = str(value).lower()
                if type(value) is None:
                    target_value = 'null'
                if type(value) == list:
                    get_target_value(value, target_key)
                if type(value) == dict:
                    get_target_value(value, target_key)

    return target_value


def substitution(data, var_dick):
    for key, value in data.items():
        if type(value) == str:
            data_var = re.search(r'\${(.*)\}', value)
            if data_var:
                try:
                    data[key] = var_dick[data_var.group(1)]
                except Exception:
                    # 如果变量不在全局字典中则赋值变量为 None
                    current_app.logger.debug('变量【' + data_var.group(1) + '】不在工程全局字典中')
                    data[key] = None
        # 处理value为列表的情况
        if type(value) == list:
            for i in range(len(value)):
                if type(value[i]) == str:
                    data_var = re.search(r'\${(.*)\}', value[i])
                    if data_var:
                        try:
                            data[key][i] = var_dick[data_var.group(1)]
                        except Exception:
                            # 如果变量不在全局字典中则赋值变量为 None
                            current_app.logger.debug('变量【' + data_var.group(1) + '】不在工程全局字典中')
                            data[key][i] = None
        # 处理value为字典的情况
        if type(value) == dict:
            for key_second, value_second in value.items():
                if type(value_second) == str:
                    data_var = re.search(r'\${(.*)\}', value_second)
                    if data_var:
                        try:
                            data[key][key_second] = var_dick[data_var.group(1)]
                        except Exception:
                            # 如果变量不在全局字典中则赋值变量为 None
                            current_app.logger.debug('变量【' + data_var.group(1) + '】不在工程全局字典中')
                            data[key][key_second] = None
