import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
'''
selenium----webdriver----common ----service----Service
                                ----by     ----By
                     ----support----excepted_conditions   
                                ----wait----WebDriverWait          
'''

# 指定驱动路径
service = Service(r'D:\Program Files (x86)\practice\seleproject\chromedriver.exe')
# 创建驱动对象
driver = webdriver.Chrome(service=service)
# 查看所有页面
print(driver.window_handles)
print(type(driver.window_handles))          # 列表
# 自由切换不同的页面
driver.switch_to.window(driver.window_handles[0])
# 获取单个页面信息
print(driver.current_window_handle)
print(type(driver.current_window_handle))   # 字符串
# # 点击“交易服务”：页面没有发生切换之前，驱动还停留在之前页面，不能操作子页面元素
# driver.find_element(By.XPATH, 'xpath').click()

# 查看所有页面
print(driver.window_handles)                # 列表
driver.switch_to.window(driver.window_handles[2])
# 点击“司法拍卖”
driver.find_element(By.XPATH, 'xpath').click()
# 获取单个页面信息
print(driver.current_window_handle)
# 查看所有页面
print(driver.window_handles)

# 强制等待
time.sleep(2)

# 关闭驱动对象
driver.close()