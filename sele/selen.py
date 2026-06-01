import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# 实例化
driver = webdriver.Chrome()
driver.implicitly_wait(5)   # 隐式等待，最大等待时间
# 调用
driver.get("https://cn.bing.com/#") # 控制
# 访问实例属性
print(driver.title)
# # 强制等待
# time.sleep(3)
# 显式等待
wait = WebDriverWait(driver,20)
wait.until(lambda d:1==1)
el = driver.find_element(By.XPATH,'//*[@id="sb_form_q"]')
print('启动的浏览器',driver)
print('定位到的元素',el)
driver.quit()
