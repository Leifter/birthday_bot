# -*- coding: UTF-8 -*-
import unittest
from get_days_to_birth_day import get_days_to_birth_day as get_days_to_birth_day
# from get_days_to_birth_day import get_days_to_birth_day_recurcive as get_days_to_birth_day
from datetime import date

class GetDaysTest(unittest.TestCase):

    def test_zero(self):
        self.assertEqual(get_days_to_birth_day(bd_date=date(year=1900, month=3, day=1), date_now=date(year=2020, month=3, day=1)), 0)

    def test_before(self):
        self.assertEqual(get_days_to_birth_day(bd_date=date(year=1900, month=3, day=31), date_now=date(year=2020, month=3, day=1)), 30)

    def test_after(self):
        self.assertEqual(get_days_to_birth_day(bd_date=date(year=2001, month=4, day=1), date_now=date(year=2020, month=3, day=1)), 31)

    def test_ves_zero(self):
        self.assertEqual(get_days_to_birth_day(bd_date=date(year=2000, month=2, day=29), date_now=date(year=2020, month=2, day=29)), 0)

    def test_ves_before_20(self):
        self.assertEqual(get_days_to_birth_day(bd_date=date(year=2000, month=2, day=29), date_now=date(year=2020, month=1, day=30)), 30)

    def test_ves_after_20(self):
        self.assertEqual(get_days_to_birth_day(bd_date=date(year=2000, month=2, day=29), date_now=date(year=2020, month=3, day=1)), 366 + 365 + 365 + 365 - 1)

    def test_ves_before_21(self):
        self.assertEqual(get_days_to_birth_day(bd_date=date(year=2000, month=2, day=29), date_now=date(year=2021, month=2, day=28)), 365 + 365 + 365 + 1)

    def test_ves_after_21(self):
        self.assertEqual(get_days_to_birth_day(bd_date=date(year=2000, month=2, day=29), date_now=date(year=2021, month=3, day=1)), 365 + 365 + 365)

    def test_ves_before_22(self):
        self.assertEqual(get_days_to_birth_day(bd_date=date(year=2000, month=2, day=29), date_now=date(year=2022, month=2, day=28)), 365 + 365 + 1)

    def test_ves_after_22(self):
        self.assertEqual(get_days_to_birth_day(bd_date=date(year=2000, month=2, day=29), date_now=date(year=2022, month=3, day=1)), 365 + 365)

    def test_ves_before_23(self):
        self.assertEqual(get_days_to_birth_day(bd_date=date(year=2000, month=2, day=29), date_now=date(year=2023, month=2, day=28)), 365 + 1)

    def test_ves_after_23(self):
        self.assertEqual(get_days_to_birth_day(bd_date=date(year=2000, month=2, day=29), date_now=date(year=2023, month=3, day=1)), 365)


if __name__ == '__main__':
    unittest.main()


