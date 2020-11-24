# -*- coding: UTF-8 -*-
from Emulator.telegram_emu import TelegramClient
from birthday_bot import ConfigParser
import datetime
import proxies

# Получить описатели диалогов
async def get_dialogs(client):
    return await client.get_dialogs()

async def get_group_id(client, title):
    return [d.id for d in (await client.get_dialogs()) if d.title == title][0]

def get_chat_members_data(client, group_title):
    with client:
        group_id = client.loop.run_until_complete(get_group_id(client, group_title))
        print("group_title = {}, group_id {}".format(group_title, group_id))
        participants = client.loop.run_until_complete(client.get_participants(group_id, aggressive=True))
    return participants

def get_chat_members_data(client, group_title):
    with client:
        dialogs = client.loop.run_until_complete(get_dialogs(client))  # Получить описатели диалогов
        group_id = client.loop.run_until_complete(get_group_id(client, group_title))
        print("group_title = {}, group_id {}".format(group_title, group_id))
        participants = client.loop.run_until_complete(client.get_participants(group_id, aggressive=True))
    return participants, group_id, dialogs

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

    # create client
    client = TelegramClient(configs["Telegram"]["session_name"],
                            int(configs["Telegram"]["api_id"]),
                            configs["Telegram"]["api_hash"], proxy=proxies.inner_proxy())
    print(client)
    group_title = "Флэйм"
    #group_id = get_group_id_loop(client, group_title)

    # dialogs = client.loop.run_until_complete(client.get_dialogs())
    with client:
        group_id = client.loop.run_until_complete(get_group_id(client, group_title))
        print("group_title = {}, group_id {}".format(group_title, group_id))
        participants = client.loop.run_until_complete(client.get_participants(group_id, aggressive=True))

    members_data, group_id, dialogs = get_chat_members_data(client, group_title)

    print(group_id)
    print(dialogs)
    print(members_data)


if __name__ == "__main__":
    main()
