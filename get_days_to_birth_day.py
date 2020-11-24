# -*- coding: UTF-8 -*-
# Определение время до ДР от текущего

import datetime


def get_days_to_birth_day(bd_date, date_now=None):
    if not bd_date:
        return None

    if not date_now:                                  # Задавать текущую дату принудительно, для отладки например
        date_now = datetime.datetime.now().date()

    ves_year_count = date_now.year % 4            # если год весокосный будет равно 0
    bd_date_next = None                           # если не в этом году, то когда
    next_year = 1                                 # Смещение следующий года, если в этои году день рождания уже было
    if bd_date.month == 2 and bd_date.day == 29:  # Для особо удачливых персон
        print("Да у нас счастливчик !!! bd_date = {}".format(bd_date))
        next_year = 4 - ves_year_count  #
        if ves_year_count != 0:  # В этом году дня рождения не будет
            bd_date_next = datetime.datetime(year=date_now.year + next_year, month=bd_date.month, day=bd_date.day).date()  # Следующий год с ДР

    if bd_date_next:  # Если точно не в этом году т.к. он весокосный, а имениннику повезло с датой ДР
        bd_date_this_year = bd_date_next
    else:             # Ищем ДР в этом году
        bd_date_this_year = datetime.datetime(year=date_now.year, month=bd_date.month, day=bd_date.day).date()  # День рождения в этом году

    time_delta = bd_date_this_year - date_now   # Время между днем рождения сотрудника и данным моментом
    days = time_delta.days

    if days < 0:  # В этом году уже прошло
        bd_date_next = datetime.datetime(year=date_now.year + next_year, month=bd_date.month, day=bd_date.day).date() # День рождения в следующем году
        time_delta = bd_date_next - date_now  # Время между днем рождения сотрудника и данным моментом
        days = time_delta.days
    return days


def get_days_to_birth_day_recurcive(bd_date, date_now=None, bd_date_next=None):
    if not bd_date:
        return None

    if not date_now:                                  # Задавать текущую дату принудительно, для отладки например
        date_now = datetime.datetime.now().date()

    next_year = 1                                 # Смещение следующий года, если в этои году день рождания уже было
    if bd_date.month == 2 and bd_date.day == 29:  # Для особо удачливых персон
        print("Да у нас счастливчик !!! bd_date = {}".format(bd_date))
        ves_year_count = date_now.year % 4
        next_year = 4 - ves_year_count  #
        if ves_year_count != 0:  # В этом году дня рождения не будет
            bd_date_next = datetime.datetime(year=date_now.year + next_year, month=bd_date.month, day=bd_date.day).date()

    if bd_date_next:  # После рекурсивного вызова функции следующее др будет в следующем году
        bd_date_this_year = bd_date_next
    else:  # Первый вызов функции
        bd_date_this_year = datetime.datetime(year=date_now.year, month=bd_date.month, day=bd_date.day).date()  # День рождения в этом году

    time_delta = bd_date_this_year - date_now   # Время между днем рождения сотрудника и данным моментом
    days = time_delta.days
    if days < 0:
        # считаем до следующего года
        return get_days_to_birth_day_recurcive(bd_date, date_now, datetime.datetime(year=bd_date_this_year.year + next_year, month=bd_date.month, day=bd_date.day).date())
    return days


if __name__ == "__main__":
    print("Тесты в tests/test/get_days_to_birth_day.py")