# -*- coding: UTF-8 -*-
# Требуется для закастыливания ошибки в открытия файлов в UNICODE для питона 3. Должны будут пофиксить в будущем. Баг известен

from petrovich.enums import Case, Gender
from petrovich.main import Petrovich, DEFAULT_RULES_PATH
import json
import os

class Case(Case):
    u"""
    Перечисление падежей
    """
    NORMATIVE = 100

class Petrovich(Petrovich):
    def __init__(self, rules_path=None):
        u"""
        :param rules_path: Путь до файла с правилами.
            В случае отсутствия будет взят путь по умолчанию,
            указанный в `DEFAULT_RULES_PATH`
        :return:
        """
        if rules_path is None:
            rules_path = DEFAULT_RULES_PATH

        if not os.path.exists(rules_path):
            raise IOError((
                'File with rules {} does not exists!'
            ).format(rules_path))

        try:
            with open(rules_path, 'r', encoding='utf8') as fp:
                self.data = json.load(fp)
        except:
            with open(rules_path, 'r') as fp:
                self.data = json.load(fp)

#        with open(DEFAULT_RULES_PATH, 'r') as fp: # Старая версия
#            self.data = json.load(fp)             # Старая версия

    def firstname(self, value, case, gender=None):
        if case == Case.NORMATIVE:
            return value
        else:
            return super().firstname(value, case, gender)


    def lastname(self, value, case, gender=None):
        if case == Case.NORMATIVE:
            return value
        else:
            return super().lastname(value, case, gender)



if __name__ == "__main__":
    p = Petrovich()
    print(p.firstname("Александр", case=Case.DATIVE))
    print(p.firstname(u"Александр", case=Case.ACCUSATIVE))
    #    print(p.firstname(u"Александр", case=Case.CASES))
    print(p.firstname(u"Александр", case=Case.INSTRUMENTAL))
    print(p.firstname(u"Александр", case=Case.PREPOSITIONAL))

