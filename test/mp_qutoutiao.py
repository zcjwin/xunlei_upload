import sys
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.keys import Keys #引入Keys类包
import time
import re, os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Qtoutiao(object):
    def __init__(self):
        self.url = 'https://mp.qutoutiao.net/login'
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get(self.url)
        self.driver.find_element_by_xpath('//input[@type="text"]').send_keys('13303774172')
        self.driver.find_element_by_xpath('//input[@type="password"]').send_keys('hong184')
        self.driver.find_element_by_id('submit-login').click()
        time.sleep(0.2)
        self.atlas()

    def atlas(self):
        self.driver.get('https://mp.qutoutiao.net/publish-content/atlas')
        self.driver.find_elements_by_xpath('//input[@type="file"]')[0].send_keys(r'C:\Users\Administrator\Desktop\tuji\qt.jpg')
        # self.driver.find_elements_by_xpath('//input[@type="file"]')[1].send_keys(r'C:\Users\Administrator\Desktop\有一种“欺骗”叫韩红, 20年捐款金额曝光, 网友：看错人了.jpg')

    def upload(self):
        pass


if __name__ == '__main__':
    mp = Qtoutiao()
    mp.login()




























