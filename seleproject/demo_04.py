from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time

from selenium.webdriver.common.by import By

# 指定驱动路径
service = Service(r'/seleproject/chromedriver.exe')
# 创建驱动对象
driver = webdriver.Chrome(service=service)

# 访问被测页面
driver.get("https://www.baidu.com/")

# 页面最大化
driver.maximize_window()

# 点击登录按钮
time.sleep(1)
driver.find_element(By.XPATH, 'xpath').click()
#输入账号
time.sleep(1)
driver.find_element(By.XPATH, '账号的xpath').send_keys('111')
driver.find_element(By.XPATH, '密码的xpath').send_keys('111')
driver.find_element(By.XPATH, '登录的xpath').click()
time.sleep(1)
# print(driver.find_element(By.XPATH, '登录结果_error的文本xpath').text)
# 不管是正例还是反例的提示信息都要进行获取
# 可以通过手写xpath以**开头进行定位
text = driver.find_element(By.XPATH, '页面中的元素[starts-with(@id, "登录结果_")]的文本xpath').text
print(text)


# 强制等待
time.sleep(5)

# 关闭驱动
driver.quit()