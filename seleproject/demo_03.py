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

# 手动添加cookie信息，保持登录状态
driver.add_cookie({'name': 'PHPSESSID', 'value': 'cookie'})
# 刷新页面清除缓存
driver.refresh()

# 当元素再子页面的frame元素中需要进行切换定位
driver.switch_to.frame(driver.find_element(By.XPATH, 'iframe'))
driver.find_element(By.XPATH, 'xpath').click()
# 强制等待
time.sleep(5)

# 关闭驱动
driver.quit()
