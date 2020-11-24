# -*- coding: UTF-8 -*-
import asyncio
import traceback
from data import config      # Конфигурация бота

from petrovich_hotfix import Petrovich, Case                       # Отремонтированный Петрович

from telegram_user import TelegramUser

from get_days_to_birth_day import get_days_to_birth_day
from commands import feed_back_handler, update_users, send_big_text
from bot_status import BOT_STATUS

PASSIVE_ONLY = False   # Для отладки пассивного режима только
EMULATION = False      # Режим эмуляции
DEBUG_ID = None        # ID для отсылки в телеграмм отладочной информации

if EMULATION:
    from Emulator.telegram_emu import TelegramClient, ErrorNoGroupFound
    from Emulator.message_emu import CreateChatRequest
    import Emulator.datetime_emu as datetime
    TIME_POLL = 0.1  # Интервал проверки ДР в сек
    from telethon import events  # Недоэмулировано!!!

else:
    from telethon import TelegramClient, events
    from telethon.tl.functions.messages import CreateChatRequest, DeleteChatUserRequest  # Функция формирования запроса пользователям на добавление в чат и удаления чата
    import datetime
    TIME_POLL = 3600  # Интервал проверки ДР в сек
    # import Emulator.datetime_emu as datetime
    # TIME_POLL = 0.1  # Интервал проверки ДР в сек


# Скланение имен по падежам. Из-за того, что имеются множественные ошибки. пришлось поменять падеж на именительный
def inflect_names(emps, case=Case.NORMATIVE):
    result_str = str()
    p = Petrovich()
    sorted_names = sorted(emps, key=lambda emp: emp.name)

    names = []
    for name in sorted_names:
        try:
            case_name = p.firstname(name.name, case, gender=name.gender)
        except ValueError:
            case_name = ""

        try:
            case_surname = p.lastname(name.surname, case, gender=name.gender)
        except ValueError:
            case_surname = ""
        names.append("{} {}".format(case_name, case_surname))

    if len(names) == 1:
        result_str = names[0]
    elif len(names) > 1:
        result_str = f'{", ".join(names[:-1])} и {names[-1]}'
    return result_str


# Проверить, что при создании группы не будет конфликтов
def check_conflicts(emps_with_bd, emps_for_new_bd_group):
    for emp_with in emps_for_new_bd_group:
        if emp_with in emps_with_bd:
            print("check_conflicts 1: {}".format(emp_with))
            return True

    for emp_without in emps_with_bd:
        if emp_without in emps_for_new_bd_group:
            print("check_conflicts 2: {}".format(emp_without))
            return True

    emps_with_bd_ids = TelegramUser.get_ids(emps_with_bd)
    emps_without_bd_ids = TelegramUser.get_ids(emps_for_new_bd_group)

    # Проверка на то, что id сотрудников без др нет в списке с id сотрудников с др. id = None не проверяется
    for emp_without_bd_id in emps_without_bd_ids:
        if emp_without_bd_id in emps_with_bd_ids and emp_without_bd_id is not None:
            print("check_conflicts 3: {}".format(emp_without_bd_id))
            return True

    # Проверка на то, что id сотрудников с др нет в списке с id сотрудников без др. id = None не проверяется
    for emp_without_id in emps_with_bd_ids:
        if emp_without_id in emps_without_bd_ids and emp_without_id is not None:
            print("check_conflicts 4: {}".format(emp_without_id))
            return True

    return False


def form_birth_days_string(emps):
    b_date_times = set([e.b_date_time for e in emps])
    b_days = [b_date_time.strftime("%d/%m") for b_date_time in b_date_times]
    return ", ".join(b_days)


# Создание группы дня рождения
async def create_bd_group(client, emps_with_bd, emps_for_new_bd_group):
    if check_conflicts(emps_with_bd, emps_for_new_bd_group):
        await debug_message(client, "<Error> create_bd_group: Ошибка проверки конфликтов участников")
        return

    # create conferense
    names_str = inflect_names(emps_with_bd)
    # print(f"create_bd_group: In {days_to_birth_day} days a birthday of {names_str}")
    group_tile = "{} День Рождения празднует {}".format(form_birth_days_string(emps_with_bd), names_str)
    # Создать конференцию из всех пользователей chat_members, кроме именинника
    members_list = "\n".join([str(m) for m in emps_for_new_bd_group])
    print("\ncreate_bd_group: Создается группа празднования ДР {} со следующими участниками\n{}\n".format(names_str, members_list))

    emps_for_new_bd_group_ids = [m.id for m in emps_for_new_bd_group if m.id]      # Получить ID, кого приглашать в группу
    new_conf_id = await create_conf(client, group_tile, emps_for_new_bd_group_ids)
    for emp in emps_with_bd:  # Заполнить атрибут группы дня рождения у сотрудников
        emp.b_group_id = new_conf_id

    await client.send_message(new_conf_id, "DB_BOT: Всем привет, Скоро ({}) День Рождения празднует {}".format(form_birth_days_string(emps_with_bd), names_str))
    return new_conf_id


# Создание группы
async def create_conf(client, title, user_ids):
    if len(title) > 120:
        title = title[:120 + 1]

    awailable_ids = []
    for id in user_ids:  # Написать проверку доступности пользователя
        print("id = {}".format(id))
        try:  # Проверяем доступность пользователей
            ent = await client.get_entity(id)
            # print(ent)
            awailable_ids.append(id)
        except:
            print("id: {} not awailable".format(id))

    group = await client(CreateChatRequest(awailable_ids, title))
#    group = 0
    print(group)
    group_id = group.chats[0].id
    return group_id


# Обнулить в БД данные старых групп
def clean_old_groups(client, employees, date_now):
    for emp in employees:  # Смотрим, чьи группы дней рождения устарели
        bd_date = emp.b_date_time
        if not bd_date:
            continue
        if get_days_to_birth_day(bd_date, date_now) >= 30:  # Обнуляем ID группы сотрудника, чей ДР был давно
            if emp.b_group_id != 0:
                if EMULATION:
                    try:
                        print("<Emulator> Обнуляются данные по группе {}".format(client.emu_def_get_dialog_by_id(emp.b_group_id)))
                    except ErrorNoGroupFound:
                        print("<Emulator> Обнуляются данные по группе {}".format(emp.b_group_id))
                emp.b_group_id = 0


# Задержка ???
async def wakeup(sleep_time=1):
    while True:
        await asyncio.sleep(sleep_time)


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


# Проанализировать текущую дату на предмет дней рождений. TODO Вместо возврата сетов, лучше переделать на пометки у пользователей
def analyze_day(employees, date_now, delay_in_days):
    emps_with_bd = set()               # Набор сотрудников у которых в ближайшее время ДР
    emps_for_new_bd_group = set()      # Набор сотрудников у которых ДР не в ближайшее время
    emps_not_celebrate = set()         # Набор сотрудников
    emps_already_created = set()       # Набор сотрудников чьи группы уже созданы
    emps_without_id = set()            # Набор сотрудников без телеги или с неизвестным ID
    emps_unknown_bd = set()            # Набор сотрудников с неизвестной датой рождения
    for emp in employees:              # Определение сотрудников у которых др
        emp.mark_b_day_today = False   # Обнулить метку того, что денб рождения сотрудника сегодня. TODO В будущем нужно переходить на метки

        if emp.b_stat == 0:         # Не добавлять сотрудкигов
            emps_not_celebrate.add(emp)
            continue

        bd_date = emp.b_date_time  # Получить дату предполагаемого дня рождения
        if not bd_date:
            emps_unknown_bd.add(emp)

        days_to_birth_day = get_days_to_birth_day(bd_date, date_now)  # Получить время до дня рождения от текущего момента

        if bd_date and days_to_birth_day <= delay_in_days:  #
            if emp.b_group_id == 0:  # Если группа с днем рождения еще не создана
                emps_with_bd.add(emp)
            else:
                emps_already_created.add(emp)
                emps_for_new_bd_group.add(emp)
                print("Группа дня рождения сотрудника уже создана : {}".format(emp))

            if days_to_birth_day == 0:          # Если день рождения сегодня
                emp.mark_b_day_today = True     # Пометить, что ДР сотрудника сегодня
        else:
            if emp.id:  # Пропускать людей без телеги
                emps_for_new_bd_group.add(emp)
            else:
                emps_without_id.add(emp)

    if emps_not_celebrate:
        pass
        # emps_list = "\n".join([str(emp) for emp in emps_not_celebrate])
        # print("День рождения данного сотрудника по тем или иным причинам проходит без особых торжеств\n{}".format(emps_list))

    return emps_with_bd, emps_for_new_bd_group, emps_already_created, emps_not_celebrate, emps_without_id, emps_unknown_bd


# Обработчик событий по дням рождениям
async def birthday_handler(client, timer_event, employees, delay_in_days, emps_file):
    # chat_members - оставим на случай варианта, если в БД будут те, кого нет в общем чате
    alive_today_count = 0                # Счетчи сколько раз за день можно посылвать alive
    today = None                         # Хранит сегодня
    BOT_STATUS.set_bd_loop_status(True)  # Установить статус бота. Обработчик дней рождения включен
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
            date_now = date_time_now.date()    # Передается при установке события. Понадобилось для отладки, чтобы datetime.datetime.now() вызывалось единожды
            print("\n\n\n -------- birthday_handler: Checking for birthday {} ---------- \n".format(date_time_now))
            # find employees with nearest birthdays

            clean_old_groups(client, employees, date_now)  # Очистить старые группы

            emps_with_bd, emps_for_new_bd_group, emps_already_created, emps_not_celebrate, emps_without_id, emps_unknown_bd \
                = analyze_day(employees=employees, date_now=date_now, delay_in_days=delay_in_days)

            if emps_unknown_bd:
                emps_list = "\n".join([str(emp) for emp in emps_unknown_bd])
                print("birthday_handler: Не найден день рождения сотрудников {}".format(emps_list))

            if not emps_with_bd:
                if not emps_already_created:
                    print("birthday_handler: В ближайшем будущем создавать группу с ДР ни у кого не планируется {}".format(date_now))
                else:
                    emps_list = "\n".join([str(emp) for emp in emps_already_created])
                    print("birthday_handler: Следующие сотрудники скоро празднуют день рождения\n{}".format(emps_list))
            else:
                await create_bd_group(client, emps_with_bd, emps_for_new_bd_group)  # Создаем группу дня рождения

            TelegramUser.save_employees_to_json(emps_file, employees)

            # Оповестить о том, что сегодня день рождения
            emps_b_day_today = [emp for emp in employees if emp.mark_b_day_today]  # Сформировать список сотрудников у кого сегодня ДР
            if len(emps_b_day_today):
                emp_0 = emps_b_day_today[0]
                b_day_group_id = emp_0.b_group_id
                b_day_today = emp_0.b_date_time.date()
                if b_day_today.month != date_now.month or b_day_today.day != date_now.day:
                    await debug_message(client, "Какая-то хрень с датами b_day_today = {}, date_now = {}".format(b_day_today, date_now))
                else:
                    await client.send_message(b_day_group_id, "DB_BOT[{}]: Всем привет! Этот День настал!".format(date_now))
                    #await debug_message(client,
                    #                          "DB_BOT[{}]: Всем привет! Этот День настал!".format(date_now))

        except asyncio.CancelledError:
            print("birthday_handler asyncio.CancelledError")
            break
        except Exception as e:
            # traceback.print_exc()
            BOT_STATUS.bd_loop_new_exception()  # Отметить новое исключение
            exc_str = "".join(traceback.format_exc())
            message = "<Error> birthday_handler: Some thing wrong {}. birthday_handler aborts".format(exc_str)
            await debug_message(client, message)
            raise e


# Отладочное сообщение
async def debug_message(client, message):
    global DEBUG_ID
    print("<Debug> " + message)
    if DEBUG_ID:
        await send_big_text(client, DEBUG_ID, message, "debug_message")
    else:
        print("Отладочное сообщение не отправлено")


# Послать сообщение, что бот работает
async def alive_message(client, timer_event):
    alive_today_count = 0  # Счетчи сколько раз за день можно посылвать alive
    today = None           # Хранит сегодня
    while True:
        await timer_event.wait()
        print("alive_message: after await timer_event.wait()")
        date_time_now = timer_event.date_time_now
        if today != date_time_now.date().day:
            today = date_time_now.date().day
            alive_today_count = 0
        else:
            alive_today_count += 1

        if alive_today_count == 0:
            await debug_message(client, "DB_BOT: Я жив !!! {}, {}".format(BOT_STATUS, timer_event.date_time_now))


# Послать себе сообщение
async def send_self_message(client, message):
    user_id = await client.get_me()                 # Получить ID текущего пользователя
    await client.send_message(user_id, message)     # Послать сообщение
    print("send_self_message: {}".format(message))


# Основнной цикл обработки события боты
def birth_day_loop(client, common_group_id, emps_file, delay_in_days, hours_to_check, chats_filter):
    # load users from file
    active = True
    if not EMULATION:
        if PASSIVE_ONLY:
            active = False
        else:
            active = input("Реальный режим работы!!! Запускать в активном режиме? Если да, то введите activate")
            if active == "activate":
                active = True
            else:
                active = False

    if PASSIVE_ONLY:
        active = False

    employees = TelegramUser.load_employees_from_json(emps_file)
    # load created groups info
    print("birth_day_loop: Loaded employees")
    print("birth_day_loop. enter")
    with client:

        # Декорируем обработчик входящих сообщений для возможности взаимодействия с ботом
        @client.on(events.NewMessage(chats=chats_filter, pattern='(?i).*bd_bot'))  # Реагировать на сообщения, содержащие pattern и только в chats_filter
        async def handler(event):
            await feed_back_handler(event, common_group_id=common_group_id, emps_file=emps_file, employees=employees)

        # Обновляем employess по новым данным из группы
        if common_group_id:  # Если общая группа определена, то обновить из нее информацию по сотрудникам
            employees = client.loop.run_until_complete(update_users(client, common_group_id, employees))
        # Отдельно получаем список всех членов гуппы
        # chat_members = client.loop.run_until_complete(get_chat_members(client, common_group_id, employees))

        tasks = []                     # Список всех задач. Могут являть собой бесконечные циклы
        timer_event = asyncio.Event()  # Событие. Выставляется когда наступает час для проверки сегодня ли ДР
        try:
            tasks.append(client.loop.create_task(wakeup()))  # need for KeyboardInterrupt
            # Основной обработчие событий дней рождения. Он же создает группы
            if active:  # Активно работать, только если это разрешено
                # Добавить основной рабочий цикл
                tasks.append(client.loop.create_task(birthday_handler(client, timer_event, employees, delay_in_days, emps_file)))
            # Добавить посылалку сообщения, что Бот жив
            tasks.append(client.loop.create_task(alive_message(client, timer_event)))
            # Добавить активатор timer_event, должен добавляться в цикл последним
            tasks.append(client.loop.create_task(hour_timer(hours_to_check, timer_event, waiting_time=TIME_POLL)))
            client.loop.run_forever()
        except KeyboardInterrupt:
            print("birth_day_loop: Finishing")
            for t in tasks:
                t.cancel()
        # client.loop.run_until_complete(client.log_out())  # don't forget about log out!
    TelegramUser.save_employees_to_json(emps_file, employees)


# Начало логики бота здесь
def init_start():
    global DEBUG_ID

    # load configs from file

    hour_to_check_start = config.hour_to_check_start  # Время начала проверки на ДР
    hour_to_check_end = config.hour_to_check_end      # !!! Не реализованно !!! Время завершения провекри на ДР
    # hour_to_check_start = datetime.datetime.now().hour
    hours_to_check = range(hour_to_check_start, hour_to_check_start + 8 + 1)      # Получить текущий час
    delay_in_days = config.delay_in_days      # Время до ДР, когда создается группа
    margin_in_days = config.margin_in_days    # !!! Не реализованно !!! Объединение ДР расположенных рядом
    emps_file = config.employees_file         # Файл с БД
    DEBUG_ID = config.debug_id                # ID для отладочный сообщений
    chats_filter = config.chats_filter        # Фильтр чатов для интерактивного взаимодействия с ботом
    common_group_id = config.common_group_id  # ИД общей группы откуда будет браться первичнаяинформация по аккаунтам именинников

    session_name = config.session_name
    api_id = config.api_id
    api_hash = config.api_hash

    proxy = config.proxy    # Прокся, если требуется
    client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)  # создаем объект для работы с Телеграмом

    # load users from file
    employees = TelegramUser.load_employees_from_json(emps_file)  # employees - множество из объектов TelegramUser
    print(employees)
    print("Loaded employees and groups")

    emps_table = TelegramUser.get_users_table(employees)
    print(emps_table)

    # Основной цикл обработки событий
    birth_day_loop(client, common_group_id, emps_file, delay_in_days, hours_to_check, chats_filter)

    return


if __name__ == "__main__":
    import main
    main.main()


