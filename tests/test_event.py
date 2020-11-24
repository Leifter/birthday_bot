# -*- coding: UTF-8 -*-
import unittest
from Emulator.telegram_emu import TelegramClient, ErrorNoGroupFound
from Emulator.message_emu import CreateChatRequest
import Emulator.datetime_emu as datetime
import proxies
import config
import asyncio
import traceback

TIME_POLL = 1  # Интервал проверки ДР в сек
from telethon import events  # Недоэмулировано!!!


# Задержка ???
async def wakeup(sleep_time=1):
    while True:
        await asyncio.sleep(sleep_time)


# Послать сообщение, что бот работает
async def alive_message(client, timer_event):
    alive_today_count = 0  # Счетчи сколько раз за день можно посылвать alive
    today = None           # Хранит сегодня
    while True:
        await timer_event.wait()
        date_time_now = timer_event.date_time_now
        print("alive_message: after await timer_event.wait() {}".format(date_time_now))
        if today != date_time_now.date().day:
            today = date_time_now.date().day
            alive_today_count = 0
        else:
            alive_today_count += 1

        if alive_today_count == 0:
            print("DB_BOT: Я жив !!! {}".format(timer_event.date_time_now))


# Обработчик событий по дням рождениям
async def birthday_handler(client, timer_event, employees, delay_in_days, emps_file):
    # chat_members - оставим на случай варианта, если в БД будут те, кого нет в общем чате
    alive_today_count = 0                # Счетчи сколько раз за день можно посылвать alive
    today = None                         # Хранит сегодня
    while True:
        try:
            await timer_event.wait()  # waiting for timer. Ожидаем наступления часа проверки того есть ли сегодня у кого-нибудь ДР
            date_time_now = timer_event.date_time_now

            if today != date_time_now.date().day:
                today = date_time_now.date().day
                alive_today_count = 0
            else:
                alive_today_count += 1

            if alive_today_count != 0:  # Не повторять проверку, если она сегодня уже делалась
                continue

            # check confs to remove
            date_time_now = timer_event.date_time_now
            print("birthday_handler: after await timer_event.wait() {}".format(date_time_now))
            date_now = date_time_now.date()    # Передается при установке события. Понадобилось для отладки, чтобы datetime.datetime.now() вызывалось единожды
            print("birthday_handler: Checking for birthday {}".format(date_time_now))

        except asyncio.CancelledError:
            print("birthday_handler asyncio.CancelledError")
            break
        except Exception as e:
            # traceback.print_exc()
            exc_str = "".join(traceback.format_exc())
            message = "<Error> birthday_handler: Some thing wrong {}. birthday_handler aborts".format(exc_str)
            print(message)
            raise e


# Установить событие, когда настал час проверки. Переделать на дианазон от и до
async def hour_timer(hours_to_check, timer_event, waiting_time=3600):
    try:
        while True:
            date_time_now = datetime.datetime.now()
            if date_time_now.time().hour in hours_to_check:
                timer_event.date_time_now = date_time_now       # Передача текущего времени в событии. Передается в birthday_handler. Это для отладки
                timer_event.set()                               # После этого сработает birthday_handler
            timer_event.clear()
            await asyncio.sleep(waiting_time)
    except asyncio.CancelledError:
        print("hour_timer: Checking time canceled")


class Test(unittest.TestCase):
    def test_timeEvents(self):

        hour_to_check_start = datetime.datetime.now().hour
        hours_to_check = range(hour_to_check_start, hour_to_check_start + 8 + 1)  # Получить текущий час
        delay_in_days = config.delay_in_days  # int(configs["DEFAULT"]["delay_in_days"])                    # Время до ДР, когда создается группа
        margin_in_days = config.margin_in_days  # int(configs["DEFAULT"]["margin_in_days"])  # Временной интервал на котором дни рождения объединяются. TODO Не реализовано
        emps_file = config.employees_file  # configs["DEFAULT"]["employees_file"]
        DEBUG_ID = config.debug_id  # int(configs["DEFAULT"]["debug_id"])
        common_group_id = config.common_group_id  # int(configs["DEFAULT"]["common_group_id"])

        session_name = config.session_name
        api_id = config.api_id
        api_hash = config.api_hash

        proxy = proxies.outer_proxy()
        client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)
        print("\n"*3)
        with client:

            tasks = []  # Список всех задач. Могут являть собой бесконечные циклы
            timer_event = asyncio.Event()  # Событие. Выставляется когда наступает час для проверки сегодня ли ДР
            try:
                tasks.append(client.loop.create_task(wakeup()))  # need for KeyboardInterrupt
                # Основной обработчие событий дней рождения. Он же создает группы
                tasks.append(client.loop.create_task(birthday_handler(client, timer_event, None, delay_in_days, emps_file)))
                tasks.append(client.loop.create_task(alive_message(client, timer_event)))  # Посылать сообщение, что Бот жив
                tasks.append(client.loop.create_task(hour_timer(hours_to_check, timer_event, waiting_time=TIME_POLL)))
                client.loop.run_forever()
            except KeyboardInterrupt:
                print("birth_day_loop: Finishing")
                for t in tasks:
                    t.cancel()
            # client.loop.run_until_complete(client.log_out())  # don't forget about log out!


if __name__ == '__main__':
    unittest.main()

