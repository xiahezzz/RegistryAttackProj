from PyQt5 import QtCore,  QtWidgets

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(493, 190)
        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(QtCore.QRect(20, 0, 181, 81))
        self.label.setObjectName("label")
        self.pwd = QtWidgets.QPlainTextEdit(dialog)
        self.pwd.setGeometry(QtCore.QRect(180, 20, 271, 41))
        self.pwd.setObjectName("pwd")
        self.recoverRegistry = QtWidgets.QPushButton(dialog)
        self.recoverRegistry.setGeometry(QtCore.QRect(270, 140, 93, 28))
        self.recoverRegistry.setObjectName("recoverRegistry")
        self.label_2 = QtWidgets.QLabel(dialog)
        self.label_2.setGeometry(QtCore.QRect(110, 60, 181, 81))
        self.label_2.setObjectName("label_2")
        self.recoverystate = QtWidgets.QPlainTextEdit(dialog)
        self.recoverystate.setGeometry(QtCore.QRect(180, 80, 271, 41))
        self.recoverystate.setObjectName("recoverystate")
        self.hiddenui = QtWidgets.QPushButton(dialog)
        self.hiddenui.setGeometry(QtCore.QRect(150, 140, 93, 28))
        self.hiddenui.setObjectName("hiddenui")

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "RegistryAttack"))
        self.label.setText(_translate("dialog", "请输入恢复注册表密码："))
        self.recoverRegistry.setText(_translate("dialog", "恢复"))
        self.label_2.setText(_translate("dialog", "恢复状态："))
        self.hiddenui.setText(_translate("dialog", "隐藏ui"))

