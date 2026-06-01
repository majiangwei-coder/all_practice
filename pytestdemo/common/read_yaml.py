# -*- conding: utf-8 -*-
import json
import os
import sys
sys.path.append(r'D:\Program Files (x86)\practice\pytestdemo\conf')
print(sys.path)
import yaml
from ..conf.setting import FILE_PATH
print(__package__)

def get_testcase_yaml(file):
    """
    获取yaml文件的数据
    :param file: yaml文件的路径
    :return: 读取到的yaml文件
    """
    try:
        with open(file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
            return yaml_data
    except Exception as e:
        print(e)


class ReadYamlData:
    """
    读取yaml数据，以及写入数据到yaml文件
    """

    def __init__(self, yaml_file=None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = '../testcase/login/login.yaml'

    def write_yaml_data(self, value):
        """
        写入数据到yaml文件
        :param value:  (dict)写入的数据
        :return:
        """
        file_path = FILE_PATH['extract']
        if not os.path.exists(file_path):
            os.system(file_path)
        file = open(file_path, mode='a', encoding='utf-8')  # a：追加写入模式；w：覆写模式
        try:
            if isinstance(value, dict):  # 判断写入的值是否是字典类型
                # 往yaml里写入数据，allow_unicode参数为False时写入中文会转成unicode，sort_keys参数为False时为按顺序写入
                write_data = yaml.dump(value, allow_unicode=True, sort_keys=False)
                file.write(write_data)
                file.close()
            else:
                print('写入到【extract.yaml】的数据必须为字典类型！')
        except Exception as e:
            print(e)
        finally:
            file.close()

    def get_extract_yaml(self, node_name):
        """
        读取接口提取的变量值
        :param node_name: yaml文件中的 key 值
        :return:
        """
        if os.path.exists(r'../extract.yaml'):
            pass
        else:
            print('extract.yaml不存在！')
            file = open('../extract.yaml', 'w')
            file.close()
            print('extract.yaml创建成功！')
        with open(r'../extract.yaml', 'r', encoding='utf-8') as f:
            extract_data = yaml.safe_load(f)
            return extract_data[node_name]


if __name__ == '__main__':
    res = get_testcase_yaml('../testcase/login/login.yaml')[0]
    url = res['baseInfo']['url']
    new_url = 'http://127.0.0.1:8787' + url
    method = res['baseInfo']['method']
    data = res['testCase'][0]['data']
    from send_requests import SendRequests

    send = SendRequests()
    res = send.run_main(method=method, url=new_url, data=data, header=None)
    # 字典类型会用双引号表示：{'error_code': None, 'msg': '登录成功', 'msg_code': 200......
    # print(type(res))
    # print(res)
    token = res.get('token')
    # print(token)
    write_data = {}
    write_data['token'] = token
    read = ReadYamlData()
    # read.write_yaml_data(write_data)
    print(read.get_extract_yaml('token'))

    # # python 常用的数据类型：str list dict set tuple
    # # json序列化和反序列化
    # # json序列化，其实就是将python的字典类型转换为字符串类型
    # json_str1 = json.dumps(res)
    # print(json_str1)  # 字符串类型会用双引号表示：{"error_code": null, "msg": "\u767b\u5f55\u6210\u529f", "msg
    # json_str2 = json.dumps(res, ensure_ascii=False)  # 改变编码格式
    # print(json_str2)  # 字符串类型会用双引号表示：{"error_code": null, "msg": "登录成功", "msg_code": 200, "org
    #
    # # json反序列化，其实就是将字符串类型转换为字典类型（变成了对象）
    # json_dict = json.loads(json_str2)
    # print(type(json_dict))
    # print(json_dict)
