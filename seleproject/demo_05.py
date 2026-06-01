from selenium import webdriver
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 1.创建一个驱动对象
# 指定驱动路径
service = Service(r'/seleproject/chromedriver.exe')
# 创建驱动对象
driver = webdriver.Chrome(service=service)
# 2.准备一个url请求地址
url = r'http://suninjie.com/'

# 3. 发送请求
driver.get(url)
driver.maximize_window()
driver.find_element(By.ID, 'xpath').click()
# 从当前页面切换到警告框里面
time.sleep(2)
alert = driver.switch_to.alert
# 获取警告框文本内容
time.sleep(2)
print(alert.text)
# # 取消警告框
# alert.dismiss()
# time.sleep(2)
# 点击确认：取消警告框
alert.accept()

# 4.睡眠3秒
time.sleep()

# 5.关闭驱动对象
driver.close()

