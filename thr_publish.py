import sys
from threading import Thread

import win32com
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys #引入Keys类包
import time
import re, os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from multiprocessing import Queue
from ua import *


path_queue = Queue()
login_status = Queue()
count_queue = Queue()
publish_queue = Queue()
run_log = {
    'path': '',
    'video_topic': '',
    'video_cate': '',
    'video_tag': '',
    'run': False
}

class XunleiPublish(object):
    count = 0
    def __init__(self):
        self.url = 'http://mp.m.xunlei.com/'

    def login(self, info):
        self.opt = webdriver.ChromeOptions()
        # self.opt.set_headless()
        # 设置随机请求头
        self.opt.add_argument('user-agent=' + getheaders())
        self.driver = webdriver.Chrome(chrome_options=self.opt,executable_path='chromedriver.exe')

        # 设置请求头
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = getheaders()
        # # 使用PhantomJS无头浏览器
        # self.driver = webdriver.PhantomJS(executable_path="./phantomjs-2.1.1-windows/bin/phantomjs.exe",
        #                              desired_capabilities=dcap)

        self.driver.get(self.url)
        time.sleep(0.1)
        uid = re.findall('^([1-9][0-9]*)', info)[0]  # 正则匹配登陆账号
        pwd = re.findall('\s+(.*?)\n', info)[0]  # 密码
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'loginIframe')))
            # 找到iframe标签
            self.driver.switch_to.frame('loginIframe')
            self.driver.find_element_by_id('al_u').send_keys(uid)
            self.driver.find_element_by_id('al_p').send_keys(pwd)
            self.driver.find_element_by_id('al_submit').click()  # 登陆按钮
            WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'loginout')))
            self.driver.find_element_by_id('loginout')
            login_dict = {'账号':uid,'状态':'登陆成功'}
            login_status.put(login_dict)
            # self.driver.get('http://mp.m.xunlei.com/publish')
        except Exception as e:
            login_dict = {'账号':uid,'状态':'登陆失败'}
            login_status.put(login_dict)
            self.driver.quit()
            sys.exit()
        self.wait_input()
        self.start_pub()
        self.upload(uid,pwd)

    # 循环等待输入标签分类
    def wait_input(self):
        while True:
            if run_log['video_topic'] and run_log['video_tag'] and run_log['path']:
                break
            time.sleep(0.1)

    # 返回开始上传按钮
    def start_pub(self):
        while True:
            if run_log['run']:
                break
            time.sleep(0.1)

    def upload(self, uid,pwd):
        self.driver.get('http://mp.m.xunlei.com/publish')
        while True:
            if not path_queue.empty():
                filepath = path_queue.get()
                # 找到input标签把所需要上传的文件发送过去
                for _ in range(10):
                    try:
                        self.driver.find_element_by_xpath('//input[@type="file"]').send_keys(filepath)
                        break
                    except:
                        self.driver.get('http://mp.m.xunlei.com/publish')
                        time.sleep(0.2)
                else:
                    self.driver.quit()
                    sys.exit()
                # 循环等待上传完成
                # while True:
                for _ in range(5000):
                    try:
                        upload_pro = self.driver.find_element_by_id('showTips'). \
                            find_element_by_tag_name('font').value_of_css_property('color')
                        if upload_pro == 'rgba(0, 128, 0, 1)':
                            break
                        elif upload_pro == 'rgba(255, 0, 0, 1)':
                            publish_dic = {'路径': filepath, '发布': '分辨率低'}
                            publish_queue.put(publish_dic)
                            os.remove(filepath)
                            self.upload(uid,pwd)
                    except:
                        time.sleep(0.2)
                else:
                    self.upload(uid,pwd)
                self.publish(filepath)
                # 分类标签如果没有分类则发布成功
                cate_attr = self.driver.find_element_by_class_name('catetxt')
                if cate_attr.text == '精确选择分类更有利于推荐':
                    self.count += 1
                    info_dict = {
                        '账号': uid,
                        '密码': '******',
                        '状态': '登陆成功',
                        '数量': self.count
                    }
                    count_queue.put(info_dict)
                    print(info_dict)
                    publish_dic = {'路径': filepath, '发布': '发布成功'}
                    publish_queue.put(publish_dic)
                    # 写入到本地文件保存上传的记录
                    with open('record.txt','a+', encoding='utf-8') as f:
                        f.write(str(info_dict)+'\n')
                    os.remove(filepath)
                else:
                    publish_dic = {'路径': filepath, '发布': '发布失败'}
                    publish_queue.put(publish_dic)
                    os.remove(filepath)
                    self.driver.refresh()
                if self.count >= 200:
                    self.driver.quit()
                    sys.exit()
            else:
                break

        self.driver.quit()
        sys.exit()

    # 填写标题、话题、分类、标签等最后发布
    def publish(self, filepath):
        title_list = re.compile('([^\x00-\xff]+)', re.S).findall(filepath)
        try:
            if title_list:
                self.driver.find_element_by_xpath('//input[@id="title"]').send_keys(','.join(title_list))
            self.driver.find_element_by_id('topicInput').send_keys(run_log['video_topic'])
            self.driver.find_element_by_class_name('span_squ').click()
            self.driver.find_elements_by_class_name('option_item')[run_log['video_cate']].click()
            self.driver.find_element_by_class_name('option_item')
            # 发送文字到input框按下回车键
            self.driver.find_element_by_id('tag-selectized').send_keys(run_log['video_tag'], Keys.ENTER)
            self.driver.find_element_by_id('prot_check').click()  # 点击同意平台服务协议按钮
            self.driver.find_element_by_id('publishBtn').click()  # 点击发布按钮
            time.sleep(2)
        except:
            pass


# 把文件路径添加到队列中
def file():
    if run_log['path']:
        for filename in os.listdir(run_log['path']):
            # filepath = run_log['path'] + '\\' + filename
            filepath = os.path.join(run_log['path'], filename)
            path_queue.put(filepath)


if __name__ == '__main__':
    pass