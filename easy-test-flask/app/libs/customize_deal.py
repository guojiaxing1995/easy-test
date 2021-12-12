import os
import re
import time


def make_deal_file(data, fun, var_dick):
    template = """
# coding:utf-8
interface_return = {{data}}
var_dick = {{var_all}}

    
{{fun}}
    
    
print({{fun_name}}(interface_return, var_dick))
"""

    fun_name = re.findall(r'def (.*)\(', fun)[0]
    r = template.replace('{{data}}', data).replace('{{var_all}}', var_dick).replace('{{fun}}', fun).\
        replace('{{fun_name}}', fun_name)

    # 将文件的true替换为True，false替换为False
    replace_true = re.sub('true', 'True', r)
    replace_false = re.sub('false', 'False', replace_true)
    content = replace_false

    tmp_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/document/tmp/'
    if not os.path.exists(tmp_directory):
        os.makedirs(tmp_directory)
    file_name = fun_name + '_' + str(int(time.time() * 1000000)) + '.py'
    path = tmp_directory + file_name

    f = open(path, 'w', encoding='utf-8')
    f.write(content)
    f.close()

    return path


def remove_deal_file(path):
    if os.path.exists(path):
        os.remove(path)

