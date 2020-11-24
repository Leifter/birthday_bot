# -*- coding:utf-8 -*-
# Стартовый файл. Обслуживает логгировние и перехват исключений

import os
import sys
from Logger import logger
import birthday_bot
import datetime               # Настоящие datetime!!! Эмуляции не происходит


# Получить имя лог-файла
def get_path_logger_file(script_name):

    # проверкак каталога логов
    catalog = u"Logs"

    if not os.path.exists(catalog):
        os.mkdir(catalog)

    # создаем экземпляр логгера
    start_sys_time = datetime.datetime.now()  # Получить текущее время

    # Получить название текущего скрипта без .py на конце # имя файла лога
    temp_file_name = os.path.basename(script_name).replace(".py", "")
    logger_file_name = u"{}_{}.log".format(temp_file_name, start_sys_time.strftime("%Y_%m_%d_%H_%M_%S"))

    return {"path": catalog + os.sep + logger_file_name, "time": start_sys_time}


# Перехватчик прерываний, для внесения текста прерываний в лог
def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    # traceback.print_exception(exc_type, exc_value, tb)
    exc_str = traceback.format_exception(exc_type, exc_value, tb)
    print("".join(exc_str))
    #input("Press Enter to exit.")
    print("Quiting...")
    sys.exit(-1)


def main():
    # reload(sys)
    # sys.setdefaultencoding('cp1251')  # Устанавливаем кодировку вывода консоли.

    sys.excepthook = show_exception_and_exit  # Перехват исключения чтобы не закрывалось окно выполнения

    temp = get_path_logger_file(__file__)
    logger_instance = logger.Logger(temp["path"])

    birthday_bot.init_start()

    logger_instance.closeLogger()


if __name__ == "__main__":
    main()
