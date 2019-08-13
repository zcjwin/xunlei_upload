import json
import os, re


# path = r'E:\funny\2019-08-08-wang'
# path = input('请输入路径：')
# for filename in os.listdir(path):
#     print(filename)
#     title_list = re.compile('([^\x00-\xff]+)', re.S).findall(filename)
#     title_list = re.compile('([^\x00-\xff]+)', re.S).findall(path + '\\' + filename)
#     if title_list:
#         print(title_list)
#         print(','.join(title_list))


with open('../account_info.txt', 'r', encoding='utf-8') as f:
    s = f.readlines()
    # print(s)
    for i in s:
        uid = re.findall('^([1-9][0-9]*)',i)
        pwd = re.findall('\s+(.*?)\n', i)
        # print('账号：',uid,'密码：',pwd)


import requests

def get_video():
    url = 'https://api.amemv.com/aweme/v1/aweme/post/?version_code=7.2.1&pass-region=1&pass-route=1&js_sdk_version=1.17.4.1&app_name=aweme&vid=1E18CEE3-FEB2-454F-B246-438B5E5C503B&app_version=7.2.1&device_id=68388168064&channel=App%20Store&mcc_mnc=46002&aid=1128&screen_width=1242&openudid=bae78ba56a1855ae4f7b73b85a87d9999e32abf9&os_api=18&ac=WIFI&os_version=12.4&device_platform=iphone&build_number=72100&device_type=iPhone8,2&iid=80313328660&idfa=37509108-033B-478A-BFC6-F7EEDFB980B1&min_cursor=0&user_id=101310088502&count=21&max_cursor=0'

    header = {
    'Host': 'api.amemv.com',
    'Connection': 'keep-alive',
    'x-Tt-Token': '007b20d22a78e001cf658118a3b94494ebc0ff45e5b4d50d84cf1cdf045bb6f378fbafbbc270109be9b114ed87a5717c832',
    'sdk-version': '1',
    'User-Agent': 'Aweme 7.2.1 rv:72100 (iPhone; iOS 12.4; zh_CN) Cronet',
    'x-tt-trace-id': '00-82640fd340d63a9ea70725cc02e1a28c-82640fd340d63a9e-01',
    'Accept-Encoding': 'gzip, deflate',
    'Cookie': 'odin_tt=cd5992f1b3b19e9964af412740dd700473a927d0bb5356b9aae20097c878a06d6311cbf7dd19585e6dfd733f42ca75c4; sid_guard=7b20d22a78e001cf658118a3b94494eb%7C1563634030%7C5184000%7CWed%2C+18-Sep-2019+14%3A47%3A10+GMT; uid_tt=39401b41d4380072cc8d577b8eed70bc; sid_tt=7b20d22a78e001cf658118a3b94494eb; sessionid=7b20d22a78e001cf658118a3b94494eb; install_id=80313328660; ttreq=1$03a2b310fdd52363475a71cb793d43b526a186be',
    'X-Khronos': '1564992664',
    'X-Pods':'',
    'X-Gorgon': '8300eee00000ab89ca2be3040f4b78ae7b3861fb70db376a7534'
    }
    headers = {
        'Host': 'api.amemv.com',
        'Connection': 'keep-alive',
        'tt-request-time': '1565075269299',
        'sdk-version': '1',
        'X-SS-Cookie': 'install_id=81599085819; ttreq=1$4d8c7c4a798fd034a7509326335b163405f70804; odin_tt=51219c1f2d32ad50070131bcae49dcbf65c28085e5a20752d99cad5de4b7b521f6cb9151250eaf48b32c113c34a7b5d99eda016733ed6de010d12f78c3313cae',
        'Cookie': 'odin_tt=cd5992f1b3b19e9964af412740dd700473a927d0bb5356b9aae20097c878a06d6311cbf7dd19585e6dfd733f42ca75c4; sid_guard=7b20d22a78e001cf658118a3b94494eb%7C1563634030%7C5184000%7CWed%2C+18-Sep-2019+14%3A47%3A10+GMT; uid_tt=39401b41d4380072cc8d577b8eed70bc; sid_tt=7b20d22a78e001cf658118a3b94494eb; sessionid=7b20d22a78e001cf658118a3b94494eb; install_id=80313328660; ttreq=1$03a2b310fdd52363475a71cb793d43b526a186be; qh[360]=1',
        'User-Agent': 'Super 2.0.2 rv:2.0.2.04 (iPhone; iOS 12.4; zh_CN) Cronet',
        'Accept-Encoding': 'gzip, deflate',
        'X-Khronos': '1565083748',
        'X-Gorgon': '830079260000093c973129f0a94b79223ff56d27772ec29d3870'
    }

    res = requests.get(url,headers=headers,verify=False)
    print(res.status_code)
    res.encoding = 'utf-8'
    html = res.text
    list_dic = json.loads(html)
    for dic in list_dic:
        aweme_id = dic['aweme_id']
        title = dic['desc']

    with open('funny.json','w',encoding='utf-8') as f:
        f.write(html)

# get_video()


from PyQt5 import QtCore, QtGui, QtWidgets

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.tableWidget = QtWidgets.QTableWidget(6, 5)
        self.book_button = QtWidgets.QPushButton("Book")
        self.book_button.clicked.connect(self.book_clicked)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.tableWidget)
        lay.addWidget(self.book_button)

        self.tableWidget.setHorizontalHeaderLabels("P1 P2 P3 P4 P5 P6".split())
        self.tableWidget.setVerticalHeaderLabels("C101 C214 C320 F04 E201".split())

        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.tableWidget.setItem(i, j, item)

    @QtCore.pyqtSlot()
    def book_clicked(self):
        items = []
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if item.checkState() == QtCore.Qt.Checked:
                    items.append(item)

        for it in items:
            r = it.row()
            c = it.column()
            v, h = self.tableWidget.horizontalHeaderItem(c).text(), self.tableWidget.verticalHeaderItem(r).text()
            print(h, v)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())













