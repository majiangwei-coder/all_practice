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
driver.find_element(By.XPATH)
# 强制等待
time.sleep(5)

# 关闭驱动
driver.quit()