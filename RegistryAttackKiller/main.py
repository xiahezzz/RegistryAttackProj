import win32api
import win32con
import win32security
import sys
import os
import pywintypes
import psutil

#取得备份注册表权限
def privilege_promote_backup():
    flags = win32security.TOKEN_ADJUST_PRIVILEGES|win32security.TOKEN_QUERY
    token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    id_flag = win32security.LookupPrivilegeValue(None, win32security.SE_BACKUP_NAME)
    privilege = [(id_flag, win32security.SE_PRIVILEGE_ENABLED)]
    win32security.AdjustTokenPrivileges(token, False, privilege)

def privilege_promote_restore():
    flags = win32security.TOKEN_ADJUST_PRIVILEGES|win32security.TOKEN_QUERY
    token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    id_flag = win32security.LookupPrivilegeValue(None, win32security.SE_RESTORE_NAME)
    privilege = [(id_flag, win32security.SE_PRIVILEGE_ENABLED)]
    win32security.AdjustTokenPrivileges(token, False, privilege)

def protect_registry(main_key, sub_key, file_name):
    key = win32api.RegOpenKeyEx(main_key, sub_key, 0, win32con.KEY_ALL_ACCESS)
    try:
        win32api.RegSaveKey(key, os.path.dirname(sys.argv[0]) + '/' + file_name)
    except pywintypes.error:
        pass
    win32api.RegCloseKey(key)

def kill_self(pro_pid):
    os.system('taskkill /pid ' + str(pro_pid)  + ' -f')

if __name__ == '__main__':
    privilege_promote_backup()
    privilege_promote_restore()
    protect_registry(win32con.HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 'protect_start')
    protect_registry(win32con.HKEY_CLASSES_ROOT, 'txtfile\shell\open\command', 'protect_txtfile')



    while True:
        txt_key = win32api.RegOpenKeyEx(win32con.HKEY_CLASSES_ROOT, 'txtfile\shell\open\command', 0,
                                        win32con.KEY_ALL_ACCESS)
        txt_key_file = str(win32api.RegQueryValueEx(txt_key, '')[0])
        win32api.RegCloseKey(txt_key)
        if txt_key_file == '%systemroot%\\system32\\notepad.exe %1':
            pass
        else:
            pro_name = []
            file_pid = []
            file_list = os.listdir(os.path.dirname(txt_key_file[0:-3]))
            for file in file_list:
                if file[-3:] == 'exe':
                    pro_name.append(file)
            for process in psutil.process_iter():
                if process.name() in pro_name:
                    file_pid.append(process.pid)

            try:
                for pid in file_pid:
                    kill_self(pid)
            except PermissionError:
                pass

            os.remove(txt_key_file[0:-3])
            print('Protect Success: del\n')

            win32api.RegRestoreKey(
                win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0,
                                      win32con.KEY_ALL_ACCESS), 'protect_start', 0x00000008)
            win32api.RegRestoreKey(
                win32api.RegOpenKeyEx(win32con.HKEY_CLASSES_ROOT, 'txtfile\shell\open\command', 0,
                                      win32con.KEY_ALL_ACCESS), 'protect_txtfile', 0x00000008)
            print('Protect Success: Recovery\n')


