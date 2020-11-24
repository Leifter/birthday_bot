# -*- coding:utf-8 -*-
import os
import ctypes

# Получить свободное место на диске по имени папки
#def getFreeSpace(dir_name):
def getFreeSpace(dir_name):
    # Для Windows 2000 и пр.
    if os.name == 'nt':
        # print("asdasd")
        kernel32 = ctypes.windll.kernel32
        lpDirectoryName = ctypes.c_char_p(bytes(dir_name, encoding="UTF-8"))
        # print(dir_name)
        TotalNumberOfFreeBytes = ctypes.c_longlong(0) # Переменная для хранения возвращаемого размера свободного места
        result = kernel32.GetDiskFreeSpaceExA(lpDirectoryName, None, None, ctypes.byref(TotalNumberOfFreeBytes))
        if not result:
            raise Exception("<Error> getFreeSpace() can't get free space")
        # print("TotalNumberOfFreeBytes = %d" % TotalNumberOfFreeBytes.value)
        return TotalNumberOfFreeBytes.value
    elif os.name == 'posix': # Для Linux
        #!!!raise Exception("<Error> getFreeSpace() Linux !!! Function does not tested. Try uncomment following")
        """
        st = os.statvfs(LogDir)
        free = st.f_bavail * st.f_frsize
        # total = st.f_blocks * st.f_frsize
        # used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return free
        """
        freeb = os.statvfs(dir_name)
        return (freeb.f_bavail * freeb.f_frsize)

    else:
        raise Exception("<Error> Can\'t get operation system type")

# Получить свободное место на диске по имени файла
def getFreeSpaceByFileName(file_name):
    file_name = os.path.abspath(file_name)
    #print("file_name="+file_name)
    dir_name = os.path.dirname(file_name)
    #print("dir_name="+dir_name)
    return getFreeSpace(dir_name)

'''def getFreeSpace1(dsk):
    freeb = os.statvfs(dsk)
    return (freeb.f_bavail * freeb.f_frsize)'''


if __name__ == "__main__":
    file_name = "1.txt"
    dir_name = os.path.abspath(file_name)

    print("getFreeSpace() = %d" % getFreeSpaceByFileName(file_name))