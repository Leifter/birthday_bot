# -*- coding: UTF-8 -*-
from birthday_bot import inflect_names, form_birth_days_string, Case
from telegram_user import TelegramUser
import unittest

class BDBotTest(unittest.TestCase):

    def setUp(self):
        self.employees = TelegramUser.load_employees_from_json("../boltalka.json")
        self.employees2 = TelegramUser.load_employees_from_json("../emps.json")
        self.employees.extend(self.employees2)
        self.maxDiff=None
        print("\nStaring tests\n")

    def test_petrovich(self):
        for emp in self.employees:
            if emp.b_date:
                names_str = inflect_names([emp], case=Case.NORMATIVE)
                bot_message = "DB_BOT: Всем привет, Скоро ({}) День Рождения празднует {}".format(form_birth_days_string([emp]), names_str)
                print(bot_message)
                group_tile = f"День Рождения празднует {names_str}"
                print(group_tile)
                print()


if __name__ == '__main__':
    unittest.main()
