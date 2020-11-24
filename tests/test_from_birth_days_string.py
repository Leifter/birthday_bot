# -*- coding: UTF-8 -*-
import unittest
from birthday_bot import form_birth_days_string
from telegram_user import TelegramUser


class FormBirthDaysStringTest(unittest.TestCase):

    def setUp(self):
        self.employees = TelegramUser.load_employees_from_json("../boltalka.json")
        self.maxDiff=None
        print("\nStaring tests\n")

    def test_analize(self):
        # FIXME Тест ручной!
        emps2 = [self.employees[0], self.employees[1]]
        emps_same = [self.employees[0], self.employees[0]]
        emps_same_1 = [self.employees[0], self.employees[0], self.employees[3]]
        emps3 = [self.employees[2], self.employees[3], self.employees[4]]
        print(form_birth_days_string(emps2))
        print(form_birth_days_string(emps_same))
        print(form_birth_days_string(emps3))
        print(form_birth_days_string(emps3))



if __name__ == '__main__':
    unittest.main()
