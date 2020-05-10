import json
import re


# var_dick  变量字典  data  被处理的数据
def deal_default(var_dick, data, target_key=None, new_key=None, true_key=None):
    if type(data) == list:
        for i in data:
            deal_default(var_dick, i, target_key, new_key)
    if type(data) == dict:
        for key, value in data.items():
            if type(value) == str or type(value) == int or type(value) == bool:
                var_dick[key] = value
            if type(value) == dict:
                deal_default(var_dick, value, target_key, new_key, key)
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
    if type(data) is None:
        if target_key:
            if target_key == true_key:
                if new_key:
                    var_dick[new_key] = data
                else:
                    var_dick[true_key] = data
    if type(data) == bool:
        if target_key:
            if target_key == true_key:
                if new_key:
                    var_dick[new_key] = data
                else:
                    var_dick[true_key] = data

    return var_dick


# 获取目标value
def get_target_value(data, target_key):
    target_value = None
    if type(data) == list:
        for i in data:
            deal_default(i, target_key)
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
