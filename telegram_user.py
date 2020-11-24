# -*- coding: UTF-8 -*-
import json
import datetime
import json
import re
from petrovich_hotfix import Gender


class NoUserFound(Exception):
    pass


class DuplicatedUsersIDs(Exception):
    pass


class TelegramUser:

    def __init__(self, id, **kwargs):
        if type(id) != type(int()):
            id = None

        self.id = id
        self.num = kwargs.get("num", int())
        self.b_stat = kwargs.get("b_stat", int())
#        self.tg_nickname = kwargs.get("tg_nickname", str()) # Deprecated
        self.name = kwargs.get("name", str())
        self.surname = kwargs.get("surname", str())
        self.patronymic = kwargs.get("patronymic", str())
        self.b_date = kwargs.get("b_date", str())
        self.phone = kwargs.get("phone", str())

        self.isTelegramData = kwargs.get("isTelegramData", bool()) # Флаг наличия специфических для телеграма данных

        self.first_name = kwargs.get("first_name", str())
        self.last_name = kwargs.get("last_name", str())
        self.username = kwargs.get("username", str())
        # self.phone = kwargs.get("phone", str())
        self.b_group_id = kwargs.get("b_group_id", int())
        self.bot = kwargs.get("bot", int())
        self.gender = kwargs.get("gender", str())
        if self.gender != Gender.MALE and self.gender != Gender.FEMALE:
            self.gender = None
            print("Не определен пол {} {}".format(self.name, self.surname))

        # Оперативные поля. Не сохраняються в БД. Вычисляются по ходу дела. TODO распространить на
        self.b_date_time = None
        self.b_date_time = self.get_b_date_time(self.b_date)
        self.b_day_today_mark = False     # День рождения
        # TODO Перейти на применение меток вместо наборов в том что вокруг avalize_day
        # self.with_bd_mark = False        # Метка сотрудников у которых в ближайшее время ДР
        # self.for_new_bd_group = False    # Метка сотрудников у которых ДР не в ближайшее время
        # self.not_celebrate = False       # Метка сотрудников, которые не учавствуют
        # self.already_created = False     # Метка сотрудников чьи группы уже созданы
        # self.without_id = False          # Метка сотрудников без телеги или с неизвестным ID
        # self.unknown_bd = False          # Метка сотрудников с неизвестной датой рождения

    def get_b_date_time(self, b_date):
        try:
            b_date_time = datetime.datetime.strptime(b_date, "%d-%m")  # Если ДР в таком формате (год при этом 1900)
        except ValueError:
            try:
                b_date_time = datetime.datetime.strptime(b_date, "%d-%m-%Y")  # Если ДР в полном формате
            except ValueError:
                print("<Warning> Не удалось определить дату дня рождения для пользователя {}, b_date = {}".format(self, b_date))
                b_date_time = None
        return b_date_time

    def __repr__(self):
        name = f"{self.surname} {self.name} {self.patronymic} {self.b_date_time}"
        name_tg = f"{self.first_name} {self.last_name} {self.username}"
        name_full = f"User({self.id}: {name} tg: {name_tg})"
        return name_full

    def asdict(self):
        user_dict = {
                "id": self.id,
                "num": self.num,
                "b_stat": self.b_stat,
                # "tg_nickname" : self.tg_nickname, # Depricated
                "name": self.name,
                "surname": self.surname,
                "patronymic": self.patronymic,
                "b_date": self.b_date,
                "phone": self.phone,
                "b_group_id": self.b_group_id,
                "gender": self.gender
            }

        if self.isTelegramData or True:
            user_dict_tg = {"first_name": self.first_name,
                            "last_name": self.last_name,
                            "username": self.username,
                            "phone": self.phone,
                            "isTelegramData": self.isTelegramData}

            user_dict.update(user_dict_tg) # Добавить в словарь специфичные для телеграма данные

        return user_dict

    @staticmethod
    def get_ids_clean(users):
        ids = [u.id for u in users if type(u.id) == type(int())]
        return ids

    @staticmethod
    def get_ids(users):
        ids = [u.id for u in users]
        return ids

    @staticmethod
    def get_users_table(users, only_who_celebrate = False):
        u_rows = []
        table_form = "{:10}| {:15}| {:15}| {:15}| {:11} | {:5} | {:15} | {:15} | {:15}"
        u_rows.append(table_form.format("ID", "Ф.", "И.", "О.", "ДР", "Stat", "first_name", "last_name", "username"))
        for u in users:
            if only_who_celebrate:
                if u.b_stat == 0:  # Добавлять только тех кто празднует
                    continue
            data_list = [u.id, u.surname, u.name, u.patronymic, u.b_date, u.b_stat, u.first_name, u.last_name, u.username]
            data_list_none_clean = []
            for d in data_list: # Устранение None для форматированной строки
                if not d:
                    d = ""
                data_list_none_clean.append(d)
            u_rows.append(table_form.format(*data_list_none_clean))

        table_str = "\n".join(u_rows)
        return "```\n" + table_str + "\n```"

    @staticmethod
    def find_employee_by_id(user_id, employees):
        find_emp = None
        for e in employees:
            if e.id == user_id:
                if find_emp:
                    raise DuplicatedUsersIDs("find_employee_by_id: we have two emps with same id: {}".format(user_id))
                find_emp = e
        if not find_emp:
            raise NoUserFound("find_employee_by_id: cant find emp with id: {}".format(user_id))
        return find_emp

    @staticmethod
    def save_employees_to_json(filename, employees, encoding='utf8'):
        # Sorting by month and date value
        def sort_b_date(emp):
            try:
                bd = emp.b_date_time
                month = bd.month
                day = bd.day
            except AttributeError:
                month = 13
                day = emp.num
            return [month, day]
        employees.sort(key=sort_b_date)  # Sorting by B date
        i = 1
        for emp in employees:  # Reinumeration
            emp.num = i
            i += 1
        # print(employees)
        with open(filename, 'w', encoding=encoding) as f:
            print("save_employees_to_json: {}".format(employees))
            json.dump([e.asdict() for e in employees], f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_employees_from_json(filename, encoding='utf8'):
        employees = list()
        with open(filename, 'r', encoding=encoding) as f_json:
            for d in json.load(f_json):
                employees.append(TelegramUser(**d))
        for emp in employees:
            if type(emp.id) != type(int()):
                emp.id = None
        return employees

    @staticmethod
    def reload_employees_from_json(filename, employees, encoding='utf8'):
        employees.clear()
        employees_reloaded = TelegramUser.load_employees_from_json(filename, encoding)
        for emp in employees_reloaded:
            employees.append(emp)


