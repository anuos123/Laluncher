import os
import re
import sys
import subprocess
import threading
import time
import json
from functools import partial
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
import webbrowser
from winotify import Notification
import datetime
import getpass

version = 'v0.01'

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.resize(1000,720)
        self.setWindowTitle(f'Zuru Launch {version}')
        # self.setWindowIcon(QtGui.QIcon(f'./icons/setting.png'))
        self.setStyleSheet(
            "QMainWindow {background: rgb(50,60,76);}"
            "QLabel {font: 15pt 微软雅黑;font-weight:bold;color: rgb(96,96,96);}"
            "")
        #　timer
        print("start...")

        icons = f'./icons/logo.ico'
        json_file = './time_str.json'
        if os.path.exists(json_file):
            with open(json_file) as f:
                result = json.load(f)
            time_str = result['data']
        else:
            time_str = ['10:01', '10:02', '10:03', '10:04', '10:05', '15:01', '15:02', '15:03', '16:05', '17:01', '17:02', '17:03']

        for at in time_str:
            self.timer = QtCore.QTimer()
            self._time(at,self.timer)
            self.timer.timeout.connect(partial(self.notify,self.timer,icons))

        # Main Layout
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)

        # Menu Layout
        self.menu_widget = QtWidgets.QWidget()
        self.menu_widget.setMaximumHeight(50)
        self.menu_layout = QtWidgets.QHBoxLayout(self.menu_widget)
        menu_info = 'Hub','Update','Document','User'
        for menu in menu_info:
            if menu=='Hub':
                button = QtWidgets.QLabel(menu)
            else:
                button = QtWidgets.QPushButton()
                button.setFixedSize(100, 40)
                self.set_button_css(button)
                self.set_button_icons(button,f'./icons/{menu}.png')

            button.setObjectName(menu)
            self.menu_layout.addWidget(button)
            if isinstance(button, QtWidgets.QPushButton):
                button.clicked.connect(partial(self._menu_func,button))
        # Func Layout
        self.product_layout = QtWidgets.QHBoxLayout()

        self.func_widget = QtWidgets.QWidget()
        self.func_layout = QtWidgets.QVBoxLayout(self.func_widget)

        # self.func_widget.setMinimumWidth(50)
        module_info = 'Product','Update'
        for info in module_info:
            button = QtWidgets.QLabel(info)
            self.func_layout.addWidget(button)

        self.image_widget = QtWidgets.QWidget()
        self.image_scroll = QtWidgets.QScrollArea()
        self.image_scroll.setWidget(self.image_widget)
        self.image_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.image_scroll.setWidgetResizable(True)

        #　Software Widget
        self.maya_layout = QtWidgets.QHBoxLayout(self.image_widget)
        self.software_dict = {
                            "Blender Foundation":"Blender",
                            "Autodesk":['Maya','3DMax'],
                            "Side Effects Software": "Houdini",
                            "INRIA": "Natron",
                            "Adobe": ["Adobe Photoshop", "Adobe Premiere Pro", "Adobe After Effects"],
                        }

        self.software = 'Maya','Houdini','Blender','Natron','3ds-max','Adobe After Effects','Adobe Photoshop','Adobe Premiere','Cinema-4d','Fusion','Mocha','Nuke','Silhouette','Unity','Unreal-engine','Zbrush'
        self.software_widget = QtWidgets.QWidget()
        self.software_layout = QtWidgets.QVBoxLayout(self.software_widget)
        for company in self.software_dict.keys():
            if company=='Autodesk':
                self.soft_picker(company)
            elif company=='Adobe':
                self.soft_picker(company)

        self.maya_layout.addWidget(self.software_widget)
        self.product_layout.addWidget(self.func_widget)
        self.product_layout.addWidget(self.image_scroll)
        self.main_layout.addWidget(self.menu_widget)
        self.main_layout.addLayout(self.product_layout)
        self.setCentralWidget(self.main_widget)

    def notify(self,t,icon):
        # window弹窗
        t.stop()
        # 获取当前时间
        now = datetime.datetime.now()
        print(now)
        weekday = now.strftime("%A")
        # 获取当前用户名称
        username = getpass.getuser()
        if username == 'lvy':
            launch = 'https://kitsu.zuru.cloud/timesheets'
        else:
            launch = 'https://kitsu.zuru.cloud/my-tasks/timesheets'

        task = f'{weekday} Task'
        daily = r'每日任务'
        message = f"Hi,{username}\n现在是休息时间...\n填写{daily},才能劳逸结合..."

        toast = Notification(app_id=task,
                             title=daily,
                             msg=message,
                             icon=icon,
                             duration='long',
                             launch=launch
                             )
        toast.show()

    def _time(self,time_str,t):
        # 预设时间
        current_time = QtCore.QTime().currentTime().msecsSinceStartOfDay()
        definition_time = QtCore.QTime.fromString(time_str,'hh:mm').msecsSinceStartOfDay()
        remaining_time = definition_time - current_time
        if remaining_time<0:
            remaining_time +=24 * 60 * 60 * 1000
        t.start(remaining_time)

    def soft_picker(self,company):
        widget = QtWidgets.QWidget()
        widget.setMaximumHeight(230)
        layout = QtWidgets.QVBoxLayout(widget)
        # Autodesk 类似标签/分界线
        label = QtWidgets.QLabel(company)
        layout.addWidget(label)
        self.set_boundary(layout, QtWidgets.QFrame.HLine)
        # soft Layout
        ad_widget = QtWidgets.QWidget()
        ad_layout = QtWidgets.QHBoxLayout(ad_widget)
        for soft in self.software_dict[company]:
            app = Software(company, soft)
            cs = os.path.join(app.source,company)
            for c in os.listdir(cs):
                if c.startswith(soft):
                    ad_layout.addWidget(app)
                    # self.set_boundary(ad_layout, QtWidgets.QFrame.VLine)
        layout.addWidget(ad_widget)
        self.software_layout.addWidget(widget, alignment=QtCore.Qt.AlignTop)

    def _menu_func(self,buton):
        sender = buton.objectName()
        if sender=='Update':
            print("None")
        elif sender == 'Document':
            webs = 'https://anuos123.github.io/zuruTools.github.io/help/html/index.html'
            webbrowser.open(webs)
        elif sender == 'User':
            print("None")

    def get_current_path(self):
        return os.path.dirname(__file__)

    def set_button_icons(self,button,icon_path):
        # button set icons
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon)
        button.setIconSize(button.size())

    def set_button_css(self,button):
        # button{border/hover/pressed}
        button.setStyleSheet(
            "QPushButton {border: none;background-color: rgb(27, 29, 35); } "
            "QPushButton:hover { background-color: rgb(33, 37, 43); border-top: 28px solid rgb(33, 37, 43); } "
            "QPushButton:pressed { background-color: rgb(85, 170, 255); border-top: 28px solid rgb(85, 170, 255); }"
            )

    def set_boundary(self,layout,HV):
        # 布局分割线,HV = QFrame.HLine/QFrame.VLine
        line = QtWidgets.QFrame()
        line.setFrameShape(HV)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(line)

class Software(QtWidgets.QWidget):
    def __init__(self,company,soft):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.Window)
        self.resize(300,160)
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QHBoxLayout(self.main_widget)
        # default setting
        self.path = None
        self.version = None
        self.company = company
        self.soft = soft
        self.setStyleSheet("QComboBox {font: 12pt 微软雅黑;font-weight:bold;color: rgb(187,187,187);}"
                           "QPushButton {font: 15pt 微软雅黑;font-weight:bold;color: rgb(56,56,56);}")

        self.source = "C:\Program Files"

        self.label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(f'./icons/{self.soft}.png')
        self.label.setPixmap(pixmap)
        self.version_layout = QtWidgets.QVBoxLayout()

        self.combox = QtWidgets.QComboBox()


        self.get_soft_version()

        self.button = QtWidgets.QPushButton(r'启动')
        self.button.setObjectName('Start')

        self.main_layout.addWidget(self.label)

        self.version_layout.addWidget(self.combox)
        self.version_layout.addWidget(self.button)
        self.button.clicked.connect(self.run)
        self.main_layout.addLayout(self.version_layout)

        self.setLayout(self.main_layout)

    def get_soft_version(self):
        # 设置软件版本
        soft_path = os.path.join(self.source, self.company)
        if self.company=='Autodesk':
            if self.soft=='Maya':
                version = [v for v in os.listdir(soft_path) if v.startswith(self.soft) and re.match(r'^Maya\d+$',v)]
                if version:
                    self.combox.addItems(version)
                    self.combox.setCurrentText('Maya2022')

            elif self.soft=='3DMax':
                version = [v for v in os.listdir(soft_path) if v.startswith(self.soft)]
                if version:
                    pass
                    # self.combox.addItems(version)
                    # self.combox.setCurrentText('Maya2022')

        elif self.company=='Adobe':
            if self.soft=='Adobe Photoshop':
                version = [v for v in os.listdir(soft_path) if v.startswith(self.soft)]
                if version:
                    self.combox.addItems(version)
                    self.combox.setCurrentText(version[0])

            elif self.soft=='Adobe Premiere Pro':
                version = [v for v in os.listdir(soft_path) if v.startswith(self.soft)]
                if version:
                    self.combox.addItems(version)
                    self.combox.setCurrentText(version[0])

            elif self.soft=='Adobe After Effects':
                version = [v for v in os.listdir(soft_path) if v.startswith(self.soft)]
                if version:
                    self.combox.addItems(version)
                    self.combox.setCurrentText(version[0])

    def _Laluncher(self):
        # 软件启动
        self.button.setText('启动中...')
        self.button.setEnabled(False)
        if self.company=='Adobe':
            soft_path = os.path.join(self.source,self.company)
            for v in os.listdir(soft_path):
                if v.startswith(self.soft):
                    if self.soft=='Adobe Photoshop':
                        exe = os.path.join(soft_path, self.soft + ' ' + v.split()[-1],f'{self.soft.split()[-1]}.exe')
                    else:
                        exe = os.path.join(soft_path, self.soft + ' ' + v.split()[-1], f'{self.soft}.exe')
                    subprocess.Popen([exe])

        elif self.company=='Autodesk':
            if self.combox.currentText():
                exe = os.path.join(self.source,self.company,self.combox.currentText(),'bin',f'{self.soft.lower()}.exe').replace('\\','/')
                subprocess.Popen([exe])
        time.sleep(10)
        self.button.setText('启动')
        self.button.setEnabled(True)

    def run(self):
        thread = threading.Thread(target=self._Laluncher)
        thread.start()

if __name__ == '__main__':
    if sys.argv is None:
        sys.argv = []
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())