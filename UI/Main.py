# coding=utf-8
import os.path
import sys
sys.path.append(r'E:\python包')
sys.path.append(r'D:\SVRemmendation')

sys.path.append(os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + "."))  # 配置项目路径变量
import IO
import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject,QEvent
import welcome
import MainWnd
from GenUsers import GenUsers
import configparser
import ReadUsers
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGraphicsOpacityEffect

def SetWndIcon(Wnd):  
    Wnd.setWindowIcon(QIcon(r'C:\Users\27879\Desktop\SVRemmendation\recommend.jpg'))

class EventFilterProxy(QObject):
    def __init__(self, event_filter_func):
        super().__init__()
        self.event_filter_func = event_filter_func

    def eventFilter(self, obj, event):
        return self.event_filter_func(obj, event)

def close_welcome(thread1, thread2, wnd):  # 等待准备工作完成然后关闭欢迎窗口
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    wnd.close()
def mainwnd_event_filter(obj, event):
    if obj is widget and event.type() == QEvent.Close:
        print('保存完毕')
        ##IO.SaveToFile()
    return False  # 保持默认事件处理

if __name__ == '__main__':
    # 准备工作，启动线程
    t1 = time.time()
    import threading

    th1 = threading.Thread(target=IO.ReadFromFile, args=())
    th2 = threading.Thread(target=ReadUsers.ReadUsers, args=())

    app = QtWidgets.QApplication(sys.argv)
    widget_wel = QtWidgets.QWidget()

    th3 = threading.Thread(target=close_welcome, args=(th1, th2, widget_wel))

    welcome_wnd = welcome.Ui_Welcome()
    welcome_wnd.setupUi(widget_wel)
    widget_wel.show()

    SetWndIcon(widget_wel)  # 增加icon图标

    th3.start()
    app.exec_()  # 为欢迎页启动消息循环

    t2 = time.time()
    print('程序准备时间：%s ms' % ((t2 - t1) * 1000))

    #  进入主界面
    widget = QtWidgets.QWidget()
    main_wnd = MainWnd.Ui_MainWnd()
    main_wnd.setupUi(widget)
    event_filter_proxy = EventFilterProxy(mainwnd_event_filter)
    widget.installEventFilter(event_filter_proxy)   
    
    widget.show()

    SetWndIcon(widget)  # 增加icon图标
    exit_code = app.exec_()

    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('../Setting.ini')
    if int(config['AutoSave']['default']) == 1:
        print('开始写文件')
        IO.SaveToFile()
        print('程序退出')
    sys.exit(exit_code)  # 为主界面启动消息循环
