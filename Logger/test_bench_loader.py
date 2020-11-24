# -*- coding:utf-8 -*-

import shortClasses
import time
import logger
import datetime

startSysTime = datetime.datetime.now()                                                            #Получить текущее время
loggerFileName = __file__.split("/")[-1].replace(".py", "")                                       #Получить название текущего скрипта без .py на конце
loggerFileName = loggerFileName + "_" + str(startSysTime.strftime("%Y_%m_%d_%H_%M_%S")) + ".log"  #имя файла лога
logger_instance = logger.Logger(loggerFileName)

test_class = shortClasses.BusyClass()

counter = 0
while counter < 20:
    test_class.count_go()
    time.sleep(0.010)
    print u"\n hello"
    counter += 1

counter = 0
while counter < 10:
    counter_1 = 0
    while counter_1 < 10:
        test_class.count_go()
        time.sleep(0.010)
        counter_1 += 1
    print u"\n hello"
    counter += 1
