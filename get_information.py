# -*- coding: UTF-8 -*-
# Функции получения данных для работы

from telethon.errors.common import MultiError


# Получить описатели диалогов
async def get_dialogs(client):
    return await client.get_dialogs()


# Получить id группы из описателей диалогов
# limit - Количество диалогов, которые будут возвращены, чтобы ограничить количество запросов на сервер телеграмм
async def get_group_id(client, title, limit=None):
    client_get_dialogs = await client.get_dialogs(limit=limit)                       # Получить список описателей диалогов. Класс Dialog
    group_id = None
    for d in client_get_dialogs:
        if d.title == title:
            group_id = d.id
            break
    #group_id = [d.id for d in client_get_dialogs if d.title == title][0]  # Поиск заданоого имени в списке и возврат его ID
    return group_id


# Получить список описателей членов группы
async def get_chat_members(client, group_id, users):
    members_ids = {m.id for m in await client.get_participants(group_id)}
    return {u for u in users if u.id in members_ids}


async def get_chat_member_id(client, group_name, username=None, first_name=None, last_name=None, phone=None, limit=None):
    data_dict = dict()
    if username: data_dict["username"] = username
    if first_name: data_dict["first_name"] = first_name
    if last_name: data_dict["last_name"] = last_name
    if phone: data_dict["phone"] = phone

    if len(data_dict) == 0:
        raise Exception("get_chat_member_id: no data for search chat member")

    group_id = await get_group_id(client, group_name, limit)
    if not group_id:
        raise Exception("get_chat_member_id: group \"{}\" not found".format(group_name))
    participants = await client.get_participants(group_id, aggressive=True)
    for p in participants:
        data_match = 0
        for data_key in data_dict:
            if getattr(p, data_key) == data_dict[data_key]:
                data_match += 1
        if data_match == len(data_dict):
            return p.id
    return None




# Вспомогатиельные функции для разового получения информации из телеграмма
def get_group_id_loop(client, group_title):
    with client:
        group_id = client.loop.run_until_complete(get_group_id(client, group_title))
    return group_id


# Получить данные всех диалогов и участников, которые в них включены (для формирования отладочной БД)
def get_all_data(client, filter):
    with client:
        dialogs = client.loop.run_until_complete(get_dialogs(client))  # Получить описатели всех диалогов
        dialogs_ex = []
        for d in dialogs:
            print("Обрабатываются данные чата \"{}\"".format(d.title))
            if filter: # Не смотрим диалог, если его имя не в фильтре
                if d.title not in filter:
                    continue
            try:
                participants = client.loop.run_until_complete(client.get_participants(d.id, aggressive=True)) # Получить список участников диалога
                d.dialog_extention = participants  # Добавление данных об участниках к данным по диалогу
                dialogs_ex.append(d)
            except MultiError:
                print("<Error> Ошибка получения списка пользователей для чата \"{}\"".format(d.title))
        return dialogs_ex


def get_chat_members_data(client, group_title):
    with client:
        dialogs = client.loop.run_until_complete(get_dialogs(client))  # Получить описатели всех диалогов
        group_id = client.loop.run_until_complete(get_group_id(client, group_title))
        print("group_title = {}, group_id {}".format(group_title, group_id))
        participants = client.loop.run_until_complete(client.get_participants(group_id, aggressive=True))
    return participants, group_id, dialogs
