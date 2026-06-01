import json

from read_yaml import ReadYamlData, get_testcase_yaml

from debugtalk import DebudTalk


class BaseRequests:

    def __init__(self):
        self.read = ReadYamlData()

    def replace_load(self, data):  # 热加载
        """yaml文件替换解析有 ${} 格式的数据"""

        str_data = data
        if not isinstance(data, str):  # 判断写入的数据是否是字符串类型
            str_data = json.dumps(data, ensure_ascii=False)

        for i in range(str_data.count('${')):
            # index检测字符串是否子字符串，并找到字符串的索引位置
            if '${' in str_data in str_data:
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
                # print(start_index, end_index)
                ref_all_params = str_data[start_index:end_index + 1]
                # print(ref_all_params)
                # 取出函数名
                func_name = ref_all_params[2:ref_all_params.index('(')]
                # print(func_name)
                # 取出函数里面的参数值
                param_name = ref_all_params[ref_all_params.index('(') + 1:ref_all_params.index(')')]
                # print(param_name)
                # 传入替换的参数获取对应的值！！！！！！关键步骤！！！！！！
                # print('yaml文件替换解析前：', str_data)
                extract_data = getattr(DebudTalk(), func_name)(*param_name.split(',') if param_name else '')
                str_data = str_data.replace(ref_all_params, str(extract_data))
                # print('yaml文件替换解析后：', str_data)
        # 还原数据
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data


if __name__ == '__main__':
    data = get_testcase_yaml('login.yaml')[0]
    print(data)
    print(type(data))
    base = BaseRequests()
    res = base.replace_load(data)
    print(res)
