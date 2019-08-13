import requests

def get_video():
    url = 'http://v6-dy.ixigua.com/0c943edfe8aec48ace0f3abf9fe3b29b/5d495123/video/m/2208865dfb070c643eeb8dddf1cbf8567e611621dc08000078356f08b339/?rc=M3N2bnk8czVtbTMzOGkzM0ApdSlJMzQzOzM4MzM3MzQzMzQ1b2ZoZGY6aDxlNGVnNDQ7OGVAaUBoNXYpQGczdilAZjs0QDZpZGpqZnFhZF8tLS0tMHNzOmlBQy4xLy8wLi4uMjQzNTYtOiNhXmEuLTFeNmIxMDE1YzVjYSNvIzphLW8jOmAwbyMvLl4%3D&version_code=7.2.1&pass-region=1&pass-route=1&js_sdk_version=1.17.4.1&app_name=aweme&vid=1E18CEE3-FEB2-454F-B246-438B5E5C503B&app_version=7.2.1&device_id=68388168064&channel=App%20Store&mcc_mnc=46002&aid=1128&screen_width=1242&openudid=bae78ba56a1855ae4f7b73b85a87d9999e32abf9&os_api=18&ac=WIFI&os_version=12.4&device_platform=iphone&build_number=72100&device_type=iPhone8%2C2&iid=80313328660&idfa=37509108-033B-478A-BFC6-F7EEDFB980B1'

    res = requests.get(url)
    print(res.status_code)
    video = res.content
    with open('E:\\funny\\一次到底多少，这个视频告诉你.mp4','wb') as f:
        f.write(video)

# get_video()


from PyQt5 import QtWidgets, QtCore
import sys
from PyQt5.QtCore import *
import time


# 继承QThread
class Runthread(QtCore.QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.2)
            self._signal.emit(str(i))  # 注意这里与_signal = pyqtSignal(str)中的类型相同


class Example(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        # 按钮初始化
        self.button = QtWidgets.QPushButton('开始', self)
        self.button.setToolTip('这是一个 <b>QPushButton</b> widget')
        self.button.resize(self.button.sizeHint())
        self.button.move(120, 80)
        self.button.clicked.connect(self.start_login)  # 绑定多线程触发事件

        # 进度条设置
        self.pbar = QtWidgets.QProgressBar(self)
        self.pbar.setGeometry(50, 50, 210, 25)
        self.pbar.setValue(0)

        # 窗口初始化
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('OmegaXYZ.com')
        self.show()

        self.thread = None  # 初始化线程

    def start_login(self):
        # 创建线程
        self.thread = Runthread()
        # 连接信号
        self.thread._signal.connect(self.call_backlog)  # 进程连接回传到GUI的事件
        # 开始线程
        self.thread.start()

    def call_backlog(self, msg):
        self.pbar.setValue(int(msg))  # 将线程的参数传入进度条


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = Example()
    myshow.show()
    sys.exit(app.exec_())











