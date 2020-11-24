# -*- coding:utf-8 -*-
# Модуль отвечает за взаимодействие с ботом

import json
import re
import traceback
from get_information import *
from telegram_user import TelegramUser


DIALOG_LIMIT = 50  # Количество диалогов, которые будут возвращены, чтобы ограничить количество запросов на сервер телеграмм

GROUP_NAME = "group_name"
USERNAME = "username"
PHONE = "phone"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"

BD_BOT = "bd_bot"

HELP = "help"
REPLY = "reply"
SHOW_BD = "show_bd"
GET_GROUP_ID = "get_group_id"
GET_CHAT_MEMBER_ID = "get_chat_member_id"
UPDATE_USER_DATA = "update_user_data"
GET_ENTITY_BY_ID = "get_entity_by_id"
RELOAD_BD_DATA = "reload_bd_data"

COMMNADS_LIST = []

COMMAND_HELP_DESCR = "Получить справку: " + BD_BOT + " " + HELP
COMMAND_REPLY_DESCR = "Получить привет от бота: " + BD_BOT + " " + REPLY
COMMAND_SHOW_BD_DESCR = "Показать данные по дням рождения: " + BD_BOT + " " + SHOW_BD
COMMAND_GET_GROUP_ID_DESCR = "Получить ID группы (dialog_limit, количество искомых диалогов при поиске. Поиск начинается с самых свежих): " + BD_BOT + " " + GET_GROUP_ID + " {\"" + GROUP_NAME + "\": \"group name\", \"dialog_limit\": 50}"
COMMAND_GET_CHAT_MEMBER_ID_DESCR = "Получить из участника группы (все данные пользователя указывать не обязательно): " \
                             + BD_BOT + " " + GET_CHAT_MEMBER_ID + " {\"" + GROUP_NAME + "\": \"group name\", \"" + USERNAME + "\": \"name\", " \
                             "\"" + PHONE + "\": 8911111, \"" + FIRST_NAME + "\": \"imya\", \"" + LAST_NAME + "\": \"familiya\", \"dialog_limit\": 50}"
COMMAND_UPDATE_USER_DATA_DESCR = "Обновить данные по пользователям общей группы в базе данных: " + BD_BOT + " " + UPDATE_USER_DATA
COMMAND_GET_ENTITY_DESCR = "Получить телеграмовский объект по ID (сообщение, юзверя, чат и т.п): " + BD_BOT + " " + GET_ENTITY_BY_ID + " {\"id\": 1234567}"


class BotCommand:
    def __init__(self, mark, help_descr, async_func):
        self.mark = mark
        self.help_descr = help_descr
        self.async_func = async_func


def add_command(mark, help_descr, func):
    COMMNADS_LIST.append(BotCommand(mark, help_descr, func))


def form_command_list():
    add_command(r"(?i).*" + HELP,
                "Получить справку: " + BD_BOT + " " + HELP,
                command_help)
    add_command(r"(?i).*" + REPLY,
                "Получить привет от бота: " + BD_BOT + " " + REPLY,
                command_reply)
    add_command(r"(?i).*" + SHOW_BD,
                "Показать данные по дням рождения: " + BD_BOT + " " + SHOW_BD,
                command_show_bd)
    add_command(r"(?i).*" + GET_GROUP_ID,
                "Получить ID группы (dialog_limit, количество искомых диалогов при поиске. Поиск начинается с самых свежих): " + BD_BOT + " " + GET_GROUP_ID +
                " {\"" + GROUP_NAME + "\": \"group name\", \"dialog_limit\": 50}",
                command_get_group_id)
    add_command(r"(?i).*" + GET_CHAT_MEMBER_ID,
                "Получить из участника группы (все данные пользователя указывать не обязательно): " \
                             + BD_BOT + " " + GET_CHAT_MEMBER_ID + " {\"" + GROUP_NAME + "\": \"group name\", \"" + USERNAME + "\": \"name\", " \
                             "\"" + PHONE + "\": 8911111, \"" + FIRST_NAME + "\": \"imya\", \"" + LAST_NAME + "\": \"familiya\", \"dialog_limit\": 50}",
                command_get_chat_member_id)
    add_command(r"(?i).*" + UPDATE_USER_DATA,
                "Обновить данные по пользователям общей группы в базе данных: " + BD_BOT + " " + UPDATE_USER_DATA,
                command_update_user_data)
    add_command(r"(?i).*" + GET_ENTITY_BY_ID,
                "Получить телеграмовский объект по ID (сообщение, юзверя, чат и т.п): " + BD_BOT + " " + GET_ENTITY_BY_ID + " {\"id\": 1234567}",
                command_get_entity_by_id)
    add_command(r"(?i).*" + RELOAD_BD_DATA,
                "Повторно подгрузить данные по пользователям из файла: " + BD_BOT + " " + RELOAD_BD_DATA,
                command_reload_bd_data)


# Сформировать строку с помощью
def format_help2():
    commands_list = [c.help_descr for c in COMMNADS_LIST]
    help_string = "\n".join(commands_list)
    return help_string


async def command_help(event, **kwargs):
    return await event.reply(format_help2())


async def command_reply(event, **kwargs):
    return await event.reply('BD_BOT: I am here!')


async def send_big_text(client, id, message, caption):
    if len(message) < 4000:
        await client.send_message(id, message)
    else:
        await client.send_file(id, bytes(message, 'utf-8'), caption="Распечатка БД")


async def command_show_bd(event, **kwargs):
    employees = kwargs["employees"]
    client = event.client
    from_id = event.message.from_id
    emps_table = TelegramUser.get_users_table(employees)
    await send_big_text(client, from_id, emps_table, "Распечатка БД");


async def command_get_group_id(event, **kwargs):
    client = event.client
    message = event.pattern_match.string
    # формат сообщения должен быть в виде bd_bot get_group_id '{"group_name": "imya gruppi", "dialog_limit": 50}'
    args = parse_args(command=message, clean_str=[BD_BOT, GET_GROUP_ID])
    title = args["group_name"]
    try:
        dialog_limit = args["dialog_limit"]
    except KeyError:
        dialog_limit = DIALOG_LIMIT
    group_id = await get_group_id(client, title, limit=dialog_limit)
    print("Group ID: {}".format(group_id))
    reply_message = "Group: \"{}\" ID: {} DIALOG_LIMIT: {}".format(title, group_id, dialog_limit)
    print(reply_message)
    await event.reply(reply_message)


async def command_get_chat_member_id(event, **kwargs):
    client = event.client
    message = event.pattern_match.string

    # формат сообщения должен быть в виде bd_bot get_chat_member_id {"group_name": "group_name", "username": "name", "phone": 8911111, "first_name": "imya", "last_name": "familiya", "dialog_limit": 50}
    args = parse_args(command=message, clean_str=[BD_BOT, GET_CHAT_MEMBER_ID])
    try:
        group_name = args[GROUP_NAME]
        try:
            username = args[USERNAME]
        except KeyError:
            username = None
        try:
            first_name = args[FIRST_NAME]
        except KeyError:
            first_name = None
        try:
            last_name = args[LAST_NAME]
        except KeyError:
            last_name = None
        try:
            phone = args[PHONE]
        except KeyError:
            phone = None
        try:
            dialog_limit = args["dialog_limit"]
        except KeyError:
            dialog_limit = DIALOG_LIMIT

        user_id = await get_chat_member_id(client, group_name=group_name, username=username, first_name=first_name, last_name=last_name, phone=phone, limit=dialog_limit)
        reply_message = "UN: {} FN: {} LN: {} PN: {} ID: {} dialog_limit: {}".format(username, first_name, last_name, phone, user_id, dialog_limit)
        print(reply_message)
        await event.reply(reply_message)
    except KeyError:
        await event.reply("BD_BOT: Key \"" + GROUP_NAME + "\" not found" + GET_CHAT_MEMBER_ID + "No\n" + format_help())


async def command_update_user_data(event, **kwargs):
    client = event.client
    employees = kwargs["employees"]
    common_group_id = kwargs["common_group_id"]
    emps_file = kwargs["emps_file"]
    employees = await update_users(client=client, chat_id=common_group_id, employees=employees)
    print(employees)
    TelegramUser.save_employees_to_json(emps_file, employees)  # Сохранение списка с сотрудниками
    await event.reply("DB_BOT: User data updated")


async def command_get_entity_by_id(event, **kwargs):
    client = event.client
    message = event.pattern_match.string
    from_id = event.message.from_id
    args = parse_args(command=message, clean_str=[BD_BOT, GET_ENTITY_BY_ID])
    entity_id = args["id"]
    entity = await client.get_entity(entity_id)
    entity_str = str(entity)
    await send_big_text(client, from_id, entity_str, "Содежимое Entity: {}".format(entity_id))


async def command_reload_bd_data(event, **kwargs):
    employees = kwargs["employees"]
    emps_file = kwargs["emps_file"]
    TelegramUser.reload_employees_from_json(emps_file, employees)
    await event.reply("BD_BOT: Данные по пользователям перезагружены с жесткого диска")


# Обработчик запросов боту. От кого получать запросы задается в birthday_bot:birth_day_loop:chats_filter
async def feed_back_handler(event, **kwargs):  # kwargs:common_group_id, emps_file, employees
    try:
        common_group_id = kwargs["common_group_id"]
        print("feed_back_handler common_group_id: {}".format(common_group_id))
        message = event.pattern_match.string
        print(message)
        command_found = False
        for command in COMMNADS_LIST:  # Поиск комманды
            if command_found:
                break
            if re.match(command.mark, message):
                await command.async_func(event, **kwargs)
                command_found = True

        if not command_found:
            print("Unknown command")
            await event.reply("BD_BOT: Unknown command\n" + format_help2())
    except BaseException as error:
        error_type = type(error)
        error_message = "{}: {}".format(error_type, error)
        help_message = error_message + "\n" + format_help2()
        await event.reply(help_message)


# Распарсить аргументы
def parse_args(command, clean_str):
    for cs in clean_str:
        command = command.replace(cs, "")
    return json.loads(command)


# Сформировать строку с помощью
def format_help():
    commands_list = [COMMAND_HELP_DESCR,
                     COMMAND_REPLY_DESCR,
                     COMMAND_SHOW_BD_DESCR,
                     COMMAND_GET_GROUP_ID_DESCR,
                     COMMAND_GET_CHAT_MEMBER_ID_DESCR,
                     COMMAND_UPDATE_USER_DATA_DESCR,
                     COMMAND_GET_ENTITY_DESCR]
    help_string = "\n".join(commands_list)
    return help_string


# Вернуть список с известными и новыми в целевом чате пользователями
async def update_users(client, chat_id, employees):
    print("async def update_users")
    # chat = await client.get_entity(str(chat_id))
    # Получить данные по пользователям чата
    users = await client.get_participants(chat_id, aggressive=True)  # aggressive disables a limit in 200 members
    users = [u for u in users if not u.bot]       # Отфильтровываем ботов
    known_ids = set(emp.id for emp in employees)  # Получить список известных ID сотрудников

    for u in users:  # Добавление сотрудников с ранее неизветсными ID, которые есть в целевой группе и обновление данных по известным сотрудникам, которые есть в группе
        if u.id not in known_ids:
            # employees.add(TelegramUser(u.id))
            print("В список сотрудников добавляется пользователь {}".format(u))
            employees.append(TelegramUser(u.id, first_name=u.first_name, last_name=u.last_name, username=u.username, phone=u.phone, isTelegramData=True))
            # TODO: write to user to get info
        else:
            oldfag = TelegramUser.find_employee_by_id(u.id, employees)
            print("Пользователь {} уже имеется в списке сотрудников".format(u))
            # Внимание объекты меняются глобально в employees
            oldfag.username = u.username
            oldfag.first_name = u.first_name
            oldfag.last_name = u.last_name
            oldfag.phone = u.phone
            oldfag.isTelegramData = True

    return employees

form_command_list()  # Сформировать список с коммандами
