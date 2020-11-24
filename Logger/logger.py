# -*- coding:utf-8 -*-
import sys
import os
import re
from Logger import free_space


# Инициаллизация модуля расветки шрифта colorama
coloramaOn = False #Флаг включения colorama
try:
    import colorama
    coloramaOn = True
except:
    print(u"<Warning> Не найден модуль colorama. Подсветка вывода работать не будет")


# Для того чтобы колорама работала в PyCharm
if 'PYCHARM_HOSTED' in os.environ:
    convert = False  # in PyCharm, we should disable convert
    strip = False
    #print("Hi! You are using PyCharm")
else:
    convert = None
    strip = None

FREE_SPACE_LOG_RESERVE = 1000000000 # Зарезервировать 1Гб для файла лога


# Получить кол-во стартовый символов возврата коретки
def get_start_b_count(str):
    start_b_count = 0
    for i in str:
        if i == "\b":
            start_b_count += 1
        else:  #Пока в начале имеем символ переноса \b
            break
    return start_b_count


# Получить строку с разрешенными символами возврата коретки. Заложено
def get_b_count_clear_string(str):
    pass


# Класс перехватчика вывода в консоль
class Logger(object):
    def __init__(self, filename="log (Unknown date).txt", debugLevel = 0):
        if not self.__class__ == sys.stdout.__class__: # Проверка на то что логгер уже захватил stdout()
            #print(u"Logger:__init__")
            if coloramaOn:
                colorama.init(autoreset=True, convert=convert, strip=strip) #Инициаллизация colorama
            # Проверка наличия свободного места на диске
            freeSpace = free_space.getFreeSpaceByFileName(filename)
            if freeSpace < FREE_SPACE_LOG_RESERVE:
                message = u"<Error> Logger.__init__() Не хватает запаса места на жестком диске для ведения лога. Имя файла {}, Доступно {} байт, требуется {}".format(filename, freeSpace, FREE_SPACE_LOG_RESERVE)
                print(message)
                raise Exception("No free space for logger")

            self.debugLevel = debugLevel    # Уровень вывода отладочной информации
            self.terminal = sys.stdout      # Сохранение предыдущего stdout для вывода в терминал
            self.log = open(filename, "w")  # Открытие файла для ведения лога
            sys.stdout = self               # Перехват stdout
        else:
            # print(u"Logger: already on")
            self.stubLogger = 1  # установить флаг того, что данный логгер является заглушкой

        # Регистрациякодовых строк цветов, в зависимости от наличия модуля Colorama
        if coloramaOn:  # без подсветки
            self.colorama_Back_RED = colorama.Back.RED
            self.colorama_Fore_RED = colorama.Fore.RED
            self.colorama_Style_RESET_ALL = colorama.Style.RESET_ALL
            self.colorama_Back_YELLOW = colorama.Back.YELLOW
            self.colorama_Fore_YELLOW = colorama.Fore.YELLOW
            self.colorama_Back_GREEN = colorama.Back.GREEN
            self.colorama_Fore_GREEN = colorama.Fore.GREEN
        else:
            self.colorama_Back_RED = ""
            self.colorama_Fore_RED = ""
            self.colorama_Style_RESET_ALL = ""
            self.colorama_Back_YELLOW = ""
            self.colorama_Fore_YELLOW = ""
            self.colorama_Back_GREEN = ""
            self.colorama_Fore_GREEN = ""

        self.printToLog_skip_next_message = False        # Флаг пропуска следующего сообщения. Нужен т.к. после основного сообщения отдельно печатается \n
        self.printToTerminal_skip_next_message = False   # Флаг пропуска следующего сообщения для вывода в терминал

    def write(self, message):
        SUCCESS_MARK = r"<Success>|<Успех>"              # Регэксп сообщения об успехе
        ERROR_MARK = r"<Error>|<Ошибка>"                 # Регэксп начала ошибки
        WARNING_MARK = "<Warning>"                       # Метка начала предупреждения
        DEBUG_MARK = r"\s*<Debug \d>"                    # Регэксп начала отладочной информации
        LOG_MARK = "<Log>"                               # Метка того, что текст идет только в лог
        TMP_MARK = "<tmp>"                              # Метка для пропуска информации в консоль без записи в лог

        printToLog = True                                # Флаг печати в лог
        printToTerminal = True                           # Флаг печати в терминал

        if self.printToLog_skip_next_message:
            self.printToLog_skip_next_message = False
            if message == '\n':  # Пропустить перенос строки, после текста, который не выводился
                printToLog = False

        if self.printToTerminal_skip_next_message:
            self.printToTerminal_skip_next_message = False
            if message == '\n':  # Пропустить перенос строки, после текста, который не выводился
                printToTerminal = False

        # if type(message) is type(u""):  # Костыль, для преобразования объектов unicode в рабоче-крестьянский str
        #     messageForRegexp = message.encode(encoding='utf-8', errors='xmlcharrefreplace')
        # else:

        messageForRegexp = message

        debug_match = re.match(DEBUG_MARK, messageForRegexp)       # Получить объект регекспа
        error_match = re.match(ERROR_MARK, messageForRegexp)       # Получить объект регекспа
        success_match = re.match(SUCCESS_MARK, messageForRegexp)   # Получить объект регекспа
        tmp_match = re.match(TMP_MARK, messageForRegexp)           # Получить объект регекспа

        if success_match:
            messageToLog = message
            messageToScreen = self.colorama_Fore_GREEN + message
        elif error_match:
            # message_to_terminal = message.strip("<Error>")
            color = self.colorama_Back_RED          # + self.colorama_Fore_WHITE
            error_string = error_match.group(0)     # Получить первую найденную строку
            messageToLog = message

            if type(message) is type(u""):  # Костыль, для преобразования объектов unicode в рабоче-крестьянский str
                # messageToScreen = message.replace(unicode(error_string), u"")  # Сначала удалить метку
                # error_string = error_string.decode("UTF-8")
                messageToScreen = message.replace(error_string, u"")  # Сначала удалить метку
            else:
                messageToScreen = message.replace(error_string, "")  # Сначала удалить метку

            messageToScreen = self.colorama_Back_RED + error_string + self.colorama_Style_RESET_ALL + self.colorama_Fore_RED + messageToScreen #Добавить метку с расцветкой
        elif message.count(WARNING_MARK):
            messageToLog = message
            messageToScreen = self.colorama_Back_YELLOW + message
        elif message.count(LOG_MARK):
            messageToLog = message
            printToTerminal = False                 # Не выводить на печать
            self.printToTerminal_skip_next_message = True
        elif debug_match:                           # Если присутствует таг <Debug n>
            debug_string = debug_match.group(0)     # Получить первую найденную строку
            debugLevel = int(debug_string[-2])      # Получить заявленный уровень отладки
            messageToLog = message
            messageToScreen = self.colorama_Fore_YELLOW + message

            if debugLevel <= self.debugLevel:       # Если текущий уровень отладки больше или равен тому что заявлено в сообщении
                pass
            else: #не выводить сообщения
                printToLog=False
                printToTerminal=False
                self.printToLog_skip_next_message = True         # Пропустить следующее сообщение т.к. скорее всего это будет \n
                self.printToTerminal_skip_next_message = True
        elif tmp_match:
            printToLog = False
            printToTerminal = True
            messageToLog = ""
            messageToScreen = message.replace(TMP_MARK, "")
        else:
            messageToLog = message
            messageToScreen = message

        # if type(messageToLog) is type(u""):  # Костыль, для преобразования объектов unicode в рабоче-крестьянский str
        #     messageToLog = messageToLog.encode(encoding='utf-8', errors='xmlcharrefreplace')

        #Обработка символа возврата коретки '\b'
        if len(messageToLog) > 0:
            if messageToLog[0] == '\b':
                start_b_count = get_start_b_count(messageToLog)
                messageToLog = messageToLog[start_b_count:]  # Удаление стартовых переносов строк из исходной
                current_pos = self.log.tell()                # Получить текущую позицию в файле
                current_pos -= start_b_count                 # Отступить от текущей позиции start_b_count байт
                if current_pos < 0:                          # Если текущая позиция получилась < 0, то оставить 0
                    current_pos = 0
                self.log.seek(current_pos, 0)                # Установить новую позицию

        #self.log.write(str(list(bytearray(messageToLog)))+"\n")  # Записать побайтно в файл для отладки
        if printToLog:
            self.log.write(messageToLog)          # Записать сообщение в файл
            self.log.flush()                      # Слить данные на диск

        if printToTerminal:
            self.terminal.write(messageToScreen)  # Вывести сообещине на экран

    def flush(self):
        self.terminal.flush()
        self.log.flush()

#    def __getattr__(self, attr):
#        return getattr(self.terminal, attr)

    def closeLogger(self):
        try:
            self.stubLogger                     #Проверить является ли текущий объект логгера заглушкой и логи пишутся ранее инициаллизированным логгером
            #print(u"closeLogger stub logger")
        except:
            sys.stdout = self.terminal          #вернуть вывод stdout
            self.log.close()                    #закрываем файл с логом
            if coloramaOn:
                colorama.deinit()               #деинициаллизируем колораму
            #print(u"closeLogger")


