import random

from read_yaml import ReadYamlData


class DebudTalk:
    def __init__(self):
        self.read = ReadYamlData()

    def get_extract_order_data(self, data, randoms):
        if randoms not in [0, -1, -2]:
            return data[randoms - 1]

    def get_extract_data(self, node_name, randoms=None):
        """
        获取extract.yaml的数据
        :param node_name:   extract.yaml中的key值
        :param random: 随机读取extract.yaml中的数据
        :return:
        """
        data = self.read.get_extract_yaml(node_name)
        if randoms is not None:
            randoms = int(randoms)
            data_value = {
                randoms: self.get_extract_order_data(data, randoms),
                0: random.choice(data),  # random.choice(data)：从data中随机读取一个数据
                -1: ','.join(data),
                -2: ','.join(data).split(',')
            }
            data = data_value[randoms]
        return data

    def md5_params(self, params):
        return 'ABCDEFG' + str(params)


if __name__ == '__main__':
    debug = DebudTalk()
    print(debug.get_extract_data('product_id', 3))
