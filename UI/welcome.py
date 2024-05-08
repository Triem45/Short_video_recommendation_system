from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Welcome(object):
    def setupUi(self, Welcome):
        Welcome.setObjectName("Welcome")
        Welcome.resize(748, 521)
        self.label = QtWidgets.QLabel(Welcome)
        self.label.setGeometry(QtCore.QRect(90, 20, 581, 51))
        font = QtGui.QFont()
        font.setFamily("隶书")
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Welcome)
        self.label_3.setGeometry(QtCore.QRect(190, 430, 391, 31))
        font = QtGui.QFont()
        font.setFamily("隶书")
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Welcome)
        QtCore.QMetaObject.connectSlotsByName(Welcome)

    def retranslateUi(self, Welcome):
        _translate = QtCore.QCoreApplication.translate
        Welcome.setWindowTitle(_translate("Welcome", "数据结构大作业 短视频推荐系统"))
        self.label.setText(_translate("Welcome", "欢迎使用短视频推荐系统"))
        self.label_3.setText(_translate("Welcome", "组员 蔡昂立 吴相希 陆涵瑞"))


        # 添加背景图片
        self.label_bg = QtWidgets.QLabel(Welcome)
        self.label_bg.setGeometry(QtCore.QRect(0, 0, 748, 521))
        self.label_bg.setPixmap(QtGui.QPixmap(r'C:\Users\27879\Desktop\SVRemmendation\recommend.jpg'))  # 设置背景图片路径
        self.label_bg.setScaledContents(True)  # 让背景图片自适应窗口大小
        self.label_bg.setObjectName("label_bg")
        
        # 将背景图片置于底层
        self.label_bg.lower()




