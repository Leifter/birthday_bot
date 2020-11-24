# -*- coding: UTF-8 -*-
import unittest
from birthday_bot import analyze_day
from telegram_user import TelegramUser
from get_days_to_birth_day import get_days_to_birth_day
import datetime


class BDBotTest(unittest.TestCase):

    def setUp(self):
        self.employees = TelegramUser.load_employees_from_json("../boltalka.json")
        self.maxDiff=None
        print("\nStaring tests\n")

    def analyze_test(self, employees, date_now, delay_in_days):
        emps_with_bd = set()            # Набор сотрудников у которых в ближайшее время ДР
        emps_for_new_bd_group = set()   # Набор сотрудников у которых ДР не в ближайшее время
        emps_not_celebrate = set()      # Набор сотрудников, кто не празднует
        emps_already_created = set()    # Набор сотрудников чьи группы уже созданы
        emps_without_id = set()         # Набор сотрудников без телеги или с неизвестным ID
        emps_unknown_bd = set()         # Набор сотрудников с неизвестной датой рождения

        for emp in employees:
            if emp.b_stat == 0:
                emps_not_celebrate.add(emp)
                continue

            bd_date = emp.b_date_time
            if not bd_date:
                emps_unknown_bd.add(emp)

            days_to_birth_day = get_days_to_birth_day(bd_date, date_now)

            if bd_date and days_to_birth_day <= delay_in_days:
                if emp.b_group_id == 0:
                    emps_with_bd.add(emp)
                else:
                    emps_already_created.add(emp)
                    emps_for_new_bd_group.add(emp)
            else:
                if emp.id:
                    emps_for_new_bd_group.add(emp)
                else:
                    emps_without_id.add(emp)

        # Убеждаемся, что все сотрудники учтены
        assert (len(emps_not_celebrate) + len(emps_with_bd) + len(emps_for_new_bd_group) + len(emps_without_id)) == len(employees)
        return emps_with_bd, emps_for_new_bd_group, emps_already_created, emps_not_celebrate, emps_without_id, emps_unknown_bd

    def test_analize(self):
        date_now = datetime.datetime(year=2012, month=1, day=1, hour=1, minute=1, second=1).date()
        delay_in_days = 14
        for i in range(365*4+356):
            print("{:04}. Сегодня {}".format(i, date_now))
            emps_with_bd_a, emps_for_new_bd_group_a, emps_already_created_a, emps_not_celebrate_a, emps_without_id_a, emps_unknown_bd_a \
                = self.analyze_test(self.employees, date_now, delay_in_days)
            actual = [emps_with_bd_a, emps_for_new_bd_group_a, emps_already_created_a, emps_not_celebrate_a, emps_without_id_a, emps_unknown_bd_a]
            emps_with_bd, emps_for_new_bd_group, emps_already_created, emps_not_celebrate, emps_without_id, emps_unknown_bd\
                = analyze_day(self.employees, date_now, delay_in_days)
            expected = [emps_with_bd, emps_for_new_bd_group, emps_already_created, emps_not_celebrate, emps_without_id, emps_unknown_bd]

            # Слева Expected (значение от тестируемого объекта), справа Actual (тестовое значение)
            self.assertEqual(expected[0], actual[0], "emps_with_bd")
            self.assertEqual(expected[1], actual[1], "emps_for_new_bd_group")
            self.assertEqual(expected[2], actual[2], "emps_already_created")
            self.assertEqual(expected[3], actual[3], "emps_not_celebrate")
            self.assertEqual(expected[4], actual[4], "emps_without_id")
            self.assertEqual(expected[5], actual[5], "emps_unknown_bd")

            date_now += datetime.timedelta(days=1)


if __name__ == '__main__':
    unittest.main()
