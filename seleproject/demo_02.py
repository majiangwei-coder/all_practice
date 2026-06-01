from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 指定驱动路径
service = Service(r'/seleproject/chromedriver.exe')
# 创建驱动对象
driver = webdriver.Chrome(service=service)

# 访问被测页面
driver.get("https://www.baidu.com/")

# 页面最大化
driver.maximize_window()
driver.find_element(By.XPATH, '//*[@id="chat-textarea"]').send_keys("美女")
driver.find_element(By.XPATH, '//*[@id="chat-submit-button"]').click()

# # 显式等待————针对某一元素进行等待，以及等待该元素们组指定条件（可见、可点击等）
# # 创建等待的实例对象
# el = WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.XPATH, '//*[@id="1"]/div/h3/a/div/div/p/span/span')))
# el.click()

# 隐式等待————针对全局，只检测元素被加载到DOM树中即继续
driver.implicitly_wait(10)

# 强制等待————非常笨拙，执行速度非常影响效率
# time.sleep(3)
driver.find_element(By.XPATH,'//*[@id="1"]/div/h3/a/div/div/p/span/span').click()

# 强制等待
time.sleep(100)

# 关闭驱动
driver.quit()
