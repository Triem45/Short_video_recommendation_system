# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_user(object):
    def setupUi(self, user):
        user.setObjectName("user")
        user.resize(400, 400)
        self.Back = QtWidgets.QPushButton(user)
        self.Back.setGeometry(QtCore.QRect(290, 360, 80, 31))
        self.Back.setObjectName("Back")
        self.textEdit = QtWidgets.QTextEdit(user)
        self.textEdit.setGeometry(QtCore.QRect(6, 6, 256, 192))
        self.textEdit.setObjectName("textEdit")
        self.Next = QtWidgets.QPushButton(user)
        self.Next.setGeometry(QtCore.QRect(80, 220, 80, 31))
        self.Next.setObjectName("Next")
        self.widget_3 = QtWidgets.QWidget(user)
        self.widget_3.setGeometry(QtCore.QRect(30, 250, 188, 121))
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.widget_3)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Comment = QtWidgets.QPushButton(self.widget)
        self.Comment.setObjectName("Comment")
        self.horizontalLayout.addWidget(self.Comment)
        self.Forward = QtWidgets.QPushButton(self.widget)
        self.Forward.setObjectName("Forward")
        self.horizontalLayout.addWidget(self.Forward)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.widget_3)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Praise = QtWidgets.QPushButton(self.widget_2)
        self.Praise.setObjectName("Praise")
        self.horizontalLayout_2.addWidget(self.Praise)
        self.Marked = QtWidgets.QPushButton(self.widget_2)
        self.Marked.setObjectName("Marked")
        self.horizontalLayout_2.addWidget(self.Marked)
        self.verticalLayout.addWidget(self.widget_2)

        self.retranslateUi(user)
        self.Next.clicked.connect(self.Login) # type: ignore
        self.Comment.clicked.connect(self.Login) # type: ignore
        self.Forward.clicked.connect(self.Login) # type: ignore
        self.Praise.clicked.connect(self.Login) # type: ignore
        self.Marked.clicked.connect(self.Login) # type: ignore
        self.Back.clicked.connect(self.Login) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(user)

    def retranslateUi(self, user):
        _translate = QtCore.QCoreApplication.translate
        user.setWindowTitle(_translate("user", "短视频推荐算法"))
        self.Back.setText(_translate("user", "返回"))
        self.Next.setText(_translate("user", "下一个"))
        self.Comment.setText(_translate("user", "评论"))
        self.Forward.setText(_translate("user", "转发"))
        self.Praise.setText(_translate("user", "点赞"))
        self.Marked.setText(_translate("user", "收藏"))

    def Login(self):
        print('LBX : Login')