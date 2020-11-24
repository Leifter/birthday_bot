# -*- coding: UTF-8 -*-
from get_information import *
from telegram_chat import *
from telegram_user import *
from configparser import ConfigParser
import proxies

from telethon import TelegramClient
from telethon import connection
from telethon.tl.functions.messages import CreateChatRequest, DeleteChatUserRequest  # Функция формирования запроса пользователям на добавление в чат и удаления чата

DIALOG_LST_JSON = "dialogs.json"
USER_LST_JSON = "users.json"

def isExists(participants_list, id):
    for p in participants_list:
        if p.id == id:
            return True
    return False

# Формирование базы данных для отладки
def form_telegram_db(client, debug_dialogs_titles):
    dialogs_ex  = get_all_data(client, filter=debug_dialogs_titles)
    dialogs_base = []
    participants_base = []
    for d in dialogs_ex:
        if d.title in debug_dialogs_titles:
            participants_ids = [p.id for p in d.dialog_extention] # Получить список ID-шников участников данного диалога

            dialogs_base.append(TelegramChat(id=d.id, title=d.title, participants_ids=participants_ids))

            for p in d.dialog_extention:
                if isExists(participants_base, p.id):  # Если пользователь с данным id уже добавлялся
                    print("Пользователь находится в нескольких чатах ID: {}, first_name: {}, last_name: {}, username: {}".format(p.id, p.first_name, p.last_name, p.username))
                    continue
                participants_base.append(TelegramUser(id=p.id, num=0, b_stat=False,
                                                      first_name=p.first_name, last_name=p.last_name, username=p.username,
                                                      phone=p.phone, isTelegramData=True))

    if len(dialogs_base) != len(debug_dialogs_titles):
        print("<Warning> количество искомых чатов не совпадает с количеством найденных")

    TelegramChat.save_dialogs_to_json(DIALOG_LST_JSON, dialogs_base)
    TelegramUser.save_employees_to_json(USER_LST_JSON, participants_base)

    return

# Формирование файла с данными по чатам в строковом выражении
#def from_dialogs_lst(client):
#    members_data, group_id, dialogs = get_chat_members_data(client, group_title)

def main():
    # load configs from file
    config_ini_file = "../config.ini"
    configs = ConfigParser()
    configs.read(config_ini_file)
    # hour_to_check = int(configs["DEFAULT"]["hour_to_check"])
    hour_to_check = datetime.datetime.now().hour             # Получить текущий час
    delay_in_days = int(configs["DEFAULT"]["delay_in_days"]) # Время до
    emps_file = configs["DEFAULT"]["employees_file"]
    dump_file = configs["DEFAULT"]["dump_file"]
    group_id = int(configs["DEFAULT"]["group_id"])

    proxy = proxies.outer_proxy()
    proxy = proxies.inner_proxy() # Получить внутренний проксисервер
    # create client
    client = TelegramClient(configs["Telegram"]["session_name"],
                            int(configs["Telegram"]["api_id"]),
                            configs["Telegram"]["api_hash"], proxy=proxy)
                            #proxy=("papaproxy.me", 433, '00000000000000000000000000000000')) #, proxy=proxy)

    debug_dialogs_titles = ["Болталка Advanced", "Новый год в Модуле 2019-2020", "Флэйм", "stepan panin"]  # Список диалогов для отладки
    form_telegram_db(client, debug_dialogs_titles) # Софрировать БД телеграмма для отладки
    #l = [TelegramUser(tg_id=123, username="asdasd", isTelegramData=True)]
    #TelegramUser.save_employees_to_json(USER_LST_JSON, l)

if __name__ == "__main__":
    main()
