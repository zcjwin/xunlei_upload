# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QMessageBox
from thr_publish import *
import sys, time

# 登陆状态线程
class Runthread(QThread):
    _signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            if not login_status.empty():
                account_dic = login_status.get()
                # print(account_dic)
                self._signal.emit(account_dic)
            time.sleep(1)

    def exit_thread(self):
        os._exit(122)

# 更新发布成功数量
class UpdateData(QThread):
    """更新数据类"""
    update_count = pyqtSignal(dict)

    def run(self):
        while True:
            if not count_queue.empty():
                _count = count_queue.get()
                self.update_count.emit(_count) # 发射信号
            time.sleep(0.2)

    def exit_thread(self):
        os._exit(122)

# 发布状态线程
class PublishStatus(QThread):
    """发布信号"""
    publish_signal = pyqtSignal(dict)

    def run(self):
        while True:
            if not publish_queue.empty():
                _status = publish_queue.get() # 从队列中取出发布状态的字典: {'路径': filepath, '发布': '发布成功'}
                self.publish_signal.emit(_status) # 发射信号
            time.sleep(0.2)

    def exit_thread(self):
        os._exit(122)

class Ui_MainWindow(QMainWindow):
    thread_list = []
    with open('film_account4.txt', 'r', encoding='utf-8') as f:
        info_list = f.readlines()

    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        # 启动登陆状态线程
        self.rthread = Runthread(self)
        self.rthread._signal.connect(self.login_status)
        self.rthread.start()

        # 启动更新上传数量线程
        self.nthread = UpdateData(self)
        self.nthread.update_count.connect(self.publish_count)
        self.nthread.start()

        # 启动发布状态线程
        self.pthread = PublishStatus(self)
        self.pthread.publish_signal.connect(self.publish_status)
        self.pthread.start()

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1110, 597)
        # 取消最大化
        MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)

        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 781, 251))
        self.tableWidget.setMidLineWidth(0)
        self.tableWidget.setIconSize(QtCore.QSize(0, 0))
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)

        # 添加数据
        for row, value in enumerate(self.info_list):
            uid = re.findall('^([1-9][0-9]*)', value)[0]
            pwd = re.findall('\s+(.*?)\n', value)[0]
            self.tableWidget.setRowCount(row+1)
            newItem = QTableWidgetItem(uid)
            self.tableWidget.setItem(row,1,newItem)
            newItem = QTableWidgetItem(pwd)
            self.tableWidget.setItem(row, 2, newItem)

            self.check = QtWidgets.QTableWidgetItem(str(row+1))
            self.check.setCheckState(QtCore.Qt.Unchecked)  # 把checkBox设为未选中状态
            self.tableWidget.setItem(row, 0, self.check)  # 在(x,y)添加checkBox

            # 表格中的数据，默认只要双击就可以修改其中的数据
            # 如果文档处于预览状态或者不可编辑状态，那就需要对表格设定为不可编辑模式
            # QTableWidget.NoEditTriggers 0 不能对表格内容进行修改
            # QTableWidget.CurrentChanged 1 任何时候都能对单元格修改
            # QTableWidget.DoubleClicked 2 双击单元格
            # QTableWidget.SelectedClicked 4 单击已选中的内容
            # QTableWidget.EditKeyPressed 8  编辑键被按下时，编辑开始
            # QTableWidget.AnyKeyPressed 16 按下任意键就能修改
            # QTableWidget.AllEditTriggers 31 以上条件全包括
            # self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

            # QTableWidget.SelectItems 0 选中单个单元格
            # QTableWidget.SelectRows 1 选中一行
            # QTableWidget.SelectColumns 2 选中一列
            self.tableWidget.setSelectionBehavior(QTableWidget.SelectItems)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)

        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(146) # 表格的平均宽度
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(22) # 表格平均高度
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)

        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 260, 781, 281))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(22)

        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(155)
        # 登陆按钮
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(900, 30, 131, 51))
        self.pushButton.setObjectName("pushButton")

        # 退出程序按钮
        self.pushButton_quit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_quit.setGeometry(QtCore.QRect(1060, 0, 51, 31))
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.pushButton_quit.clicked.connect(self.exit_quit)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(830, 114, 81, 41))
        self.label_3.setObjectName("label_3")
        # 文件路径输入框
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(900, 120, 131, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(830, 177, 75, 41))
        self.label_2.setObjectName("label_2")

        # 添加话题输入框
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(900, 180, 131, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(830, 220, 81, 89))
        self.label.setObjectName("label")
        # 下拉选择框
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(900, 250, 71, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        # 添加标签
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(830, 310, 71, 88))
        self.label_4.setObjectName("label_4")
        # 添加标签输入框
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(900, 340, 131, 31))
        self.lineEdit.setObjectName("lineEdit")

        # 确定按钮
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(830, 430, 71, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        # 开始上传按钮
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(920, 430, 111, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1110, 26))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(mainWindow)
        self.statusBar.setObjectName("statusBar")
        mainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "迅雷号"))
        self.tableWidget.setSortingEnabled(False)
        # 设置表头
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("mainWindow", "序号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("mainWindow", "账号"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("mainWindow", "密码"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("mainWindow", "登陆状态"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("mainWindow", "上传数量"))
        # item.tableWidget().horizontalHeader().setVisible(False) # 隐藏横向的表头
        item.tableWidget().verticalHeader().setVisible(False) # 隐藏垂直表头

        # 单独设置某一列表格的宽度
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(0, 55)
        self.tableWidget.horizontalHeader().setStretchLastSection(True) #列宽度占满表格(最后一个列拉伸处理沾满表格)

        # 第二个表头
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("mainWindow", "路径"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("mainWindow", "分类"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("mainWindow", "状态"))

        self.tableWidget_2.setColumnWidth(1, 150)
        self.tableWidget_2.setColumnWidth(2, 100)
        self.tableWidget_2.setColumnWidth(0, 426)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)

        self.pushButton_quit.setText(_translate("mainWindow", "退出"))
        self.pushButton.setText(_translate("mainWindow", "登陆账号"))
        self.pushButton.clicked.connect(self.login)
        self.label_3.setText(_translate("mainWindow", "文件路径："))
        self.label_2.setText(_translate("mainWindow", "添加话题："))
        self.label.setText(_translate("mainWindow", "设置分类："))
        self.comboBox.setItemText(0, _translate("mainWindow", "搞笑"))
        self.comboBox.setItemText(1, _translate("mainWindow", "美女"))
        self.comboBox.setItemText(2, _translate("mainWindow", "影视"))
        self.comboBox.setItemText(3, _translate("mainWindow", "社会"))
        self.comboBox.setItemText(4, _translate("mainWindow", "娱乐"))
        self.comboBox.setItemText(5, _translate("mainWindow", "才艺"))
        self.comboBox.setItemText(6, _translate("mainWindow", "美食"))
        self.comboBox.setItemText(7, _translate("mainWindow", "动物"))
        self.comboBox.setItemText(8, _translate("mainWindow", "奇趣"))
        self.comboBox.setItemText(9, _translate("mainWindow", "游戏"))
        self.comboBox.setItemText(10, _translate("mainWindow", "时尚"))
        self.comboBox.setItemText(11, _translate("mainWindow", "萌娃"))
        self.comboBox.setItemText(12, _translate("mainWindow", "新闻"))
        self.comboBox.setItemText(13, _translate("mainWindow", "旅游"))
        self.comboBox.setItemText(14, _translate("mainWindow", "体育"))
        self.comboBox.setItemText(15, _translate("mainWindow", "科技"))
        self.comboBox.setItemText(16, _translate("mainWindow", "动漫"))
        self.comboBox.setItemText(17, _translate("mainWindow", "教育"))
        self.comboBox.setItemText(18, _translate("mainWindow", "母婴"))
        self.comboBox.setItemText(19, _translate("mainWindow", "生活"))
        self.comboBox.setItemText(20, _translate("mainWindow", "汽车"))
        self.comboBox.setItemText(21, _translate("mainWindow", "情感"))
        self.comboBox.setItemText(22, _translate("mainWindow", "其他"))
        self.label_4.setText(_translate("mainWindow", "添加标签："))
        self.pushButton_2.setText(_translate("mainWindow", "确定"))
        self.pushButton_2.clicked.connect(self.lineEdit_function) # 确定按钮绑定获取文本框输入内容
        # self.comboBox.currentIndexChanged.connect(self.lineEdit_function) # 下拉框选择后直接返回
        self.pushButton_3.setText(_translate("mainWindow", "开始上传"))
        self.pushButton_3.clicked.connect(self.start_run)

    # 开始上传按钮
    def start_run(self):
        if run_log['path'] and run_log['video_topic'] and run_log['video_tag']:
            run_log['run'] = True
        else:
            QMessageBox.question(self, '提示', '未知的路径或类别！', QMessageBox.Ok)

    # 确定按钮绑定函数
    def lineEdit_function(self):
        run_log['path'] = self.lineEdit_2.text()
        file()
        run_log['video_topic'] = self.lineEdit_3.text()
        run_log['video_cate'] = self.comboBox.currentIndex() # 返回下拉框索引
        run_log['video_tag'] = self.lineEdit.text()

        if run_log['path'] and run_log['video_topic'] and run_log['video_tag']:
            for num, filename in enumerate(os.listdir(run_log['path'])):
                # 拼接每个视频的上传路径
                # filepath = run_log['path'] + '\\' + filename
                filepath = os.path.join(run_log['path'], filename)
                self.tableWidget_2.setRowCount(num+1)
                newItem = QTableWidgetItem(filepath)
                self.tableWidget_2.setItem(num, 0, newItem)
                newItem = QTableWidgetItem(run_log['video_topic'])
                self.tableWidget_2.setItem(num, 1, newItem)
        else:
            QMessageBox.question(self, '提示', '请输入文件路径和分类！', QMessageBox.Ok)

    # 点击登陆
    def login(self):
        u_list = [] # 账号密码信息列表
        for i in range(self.tableWidget.rowCount()):
            it = self.tableWidget.item(i, 0) # 复选框对象
            # 如果复选框是被选中状态获取到表格中的账号和密码
            if it.checkState() == QtCore.Qt.Checked:
                pitch_on_uid = self.tableWidget.item(i, 1).text()
                pitch_on_pwd = self.tableWidget.item(i, 2).text()
                uid_pwd = pitch_on_uid + '\t' + pitch_on_pwd + '\n'
                u_list.append(uid_pwd)
                # u_dic = {'账号': pitch_on_uid, '密码': pitch_on_pwd}
                # u_list.append(u_dic)
            else:
                continue

        # 开启多线程进行登陆
        if u_list:
            for info in u_list:
                mp = XunleiPublish()
                t = Thread(target=mp.login, args=(info,))
                self.thread_list.append(t)
                t.setDaemon(True)
                t.start()
        else:
            QMessageBox.question(self, '提示', '请选择要登陆账号！', QMessageBox.Ok)

    # 登陆状态的日志
    def login_status(self, account_dic):
        num_row = self.tableWidget.rowCount() # 界面显示账号的数量/表格行数
        for index in range(num_row):
            column_text = self.tableWidget.item(index, 1).text()    # qt界面表格中的账号
            # 判断界面表格中的账号是否和从队列中取出的字典中的账号是否相等
            # 如果相等就获取当前账号的索引值，把对应账号的登陆状态根据索引值填入到表格中
            if column_text == account_dic['账号']:
                newItem = QTableWidgetItem(account_dic['状态'])
                self.tableWidget.setItem(index, 3, newItem)
                break

    # 上传成功数量
    def publish_count(self, _count):
        num_row = self.tableWidget.rowCount()
        for i in range(num_row):
            column_text = self.tableWidget.item(i, 1).text()
            if column_text == _count['账号']:
                newItem = QTableWidgetItem(str(_count['数量']))
                self.tableWidget.setItem(i, 4, newItem)
                break

    # 上传状态
    def publish_status(self, _status):
        num_row = self.tableWidget_2.rowCount()
        for i in range(num_row):
            column_text = self.tableWidget_2.item(i, 0).text()
            if column_text == _status['路径']:
                newItem_2 = QTableWidgetItem(_status['发布'])
                self.tableWidget_2.setItem(i, 2, newItem_2)
                break

    # 退出程序
    def exit_quit(self):
        global EXIT_COND
        res = QMessageBox.question(self, '提示', '您确定要退出程序吗！', QMessageBox.Yes | QMessageBox.No)  # 提示框
        if res == QMessageBox.Yes:
            try:
                os.system('taskkill /im chromedriver.exe /F')  # 结束chromedriver.exe进程
                # os.system('taskkill /im chrome.exe /F')  # 结束chrome进程
                # os.system('taskkill /im ./phantomjs-2.1.1-windows/bin/phantomjs.exe /F')
            except:
                pass
            self.rthread.exit_thread()
            self.nthread.exit_thread()
            self.pthread.exit_thread()
            time.sleep(1)
            sys.exit()
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# 打包封装为.exe可执行文件 cd到文件路径下进行打包
# pyinstaller -F -w xunlei_ui.py -p thr_publish.py -p ua.py --hidden-import xunlei_ui --hidden-import thr_publish --hidden-import ua