# coding=utf-8
import os.path
import sys
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
from PyQt5.QtWidgets import QMessageBox
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
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText("是否要保存本次运行的视频数据")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        choice = msg_box.exec_()
        
        if choice == QMessageBox.Yes:
            IO.SaveToFile()
            print('保存完毕')
        elif choice == QMessageBox.No:
            print('放弃保存')
            
    return False  # 保持默认事件

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

    SetWndIcon(widget_wel) 

    th3.start()
    app.exec_()  

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

    sys.exit(exit_code)  # 为主界面启动消息循环
