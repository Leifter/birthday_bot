# -*- coding:utf-8 -*-
from Logger import logger
import os
import re
import datetime

#from __future__ import print_function

print("LoggerDOWN")

startSysTime = datetime.datetime.now()                                                            #Получить текущее время
loggerFileName = __file__.split("/")[-1].replace(".py", "")                                       #Получить название текущего скрипта без .py на конце
loggerFileName = loggerFileName + "_" + str(startSysTime.strftime("%Y_%m_%d_%H_%M_%S")) + ".log"  #имя файла лога
newLogger = logger.Logger(loggerFileName, debugLevel = 1)

print("asdsdsda")
print("<Error>lalalala")
print("<Ошибка>lalalala")
print("<Warning>la2dsfdsflalala")
print("before russian")
print(u"<Warning>Русский текст для проверки") #проверка объектов unicode
print("after russian")
print("<Warning><Error> pered isklucheniya")
#import someVarToExcept #Для генерации исключения и проверки того что последнее сообшение попалов лог
print(__file__)
print(os.path.basename(__file__))
print("  <Debug 0> Some debug message %d" % 5)
print("  <Debug 4> Some debug message %d" % 10)
print("<Log> This must be printed only in log file")
print("<Success> This must be printed only in log file")
print(u"<Успех> This must be printed only in log file")
print(u"<Error> This must be printed only in log file")
print(u"<Ошибка> This must be printed only in log file")

newLogger.closeLogger()
"""
result = re.match(r"\s*<Debug \d>", " 1 <Debug 1> <Debug> some inf")
if not result:
    print("None")
    quit()
debug_string = result.group(0)
print(debug_string)
print(debug_string[-2])
result = re.match("\d*", result.group(0))
print(result.group(0))
try:
    debugMark = result.group(0)
    print (debugMark)
except:
    print("none")
"""

"""
#Была проблема со строковыми объектами unicode
log = open("utest.txt", "w")
str_u = u"asasdasdлдывоалывоадло1\n".encode(encoding='utf-8', errors='xmlcharrefreplace')
#str = u"asasdasdлдывоалывоадло1\n"
log.write(str_u)
str_u = "asasdasdлдывоалывоадло2\n"
log.write(str_u)
quit()
"""

