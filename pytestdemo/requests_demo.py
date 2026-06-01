import requests
from requests import utils

# 1.-------------------------------------------POST
url1 = 'http://127.0.0.1:8787/dar/user/login'

header1 = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

data1 = {
    "user_name": "test01",
    "passwd": "admin123"
}

res1 = requests.post(url=url1, data=data1)
# print(res1)
# 返回文本类型的数据
# print(res1.text)
# 返回二进制内容
# print(res1.content)
# 返回json格式
# print(res1.json)

# 2.-------------------------------------------GET
url2 = 'http://127.0.0.1:8787/coupApply/cms/goodsList'

header2 = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

json_data = {
    'msgType': 'getHandsetListOfCust',
    'page': 1,
    'size': 20
}

res2 = requests.get(url = url2, params = json_data, headers = header2)      # 表单提交调用 data

# 默认返回的只是一个接口的状态码
# print(res2)
# # 需要返回文本类型的接口返回值
# print(res2.text, type(res2.text))       # 字符串
# # 需要返回json格式的值
# print(res2.json(), type(res2.json()))   # 字典

# -------------------------------------------DELETE
# requests.delete()

# -------------------------------------------PUT
# requests.put()

# 3.-------------------------------------------requests.session()会话管理
session = requests.session()

res3 = session.request(method = 'get', url = url2, params = json_data, headers = header2)
# print(res3.json())

# 4.-------------------------------------------cookie
url4 = 'http://127.0.0.1:8787/api/order/customer/orderPlan/getMaterial'

header4 = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

# cookie =

result = session.request(method = 'post', url = url1, data = data1)
cookie = requests.utils.dict_from_cookiejar(result.cookies)
# print(cookie)
# print(result.text)

