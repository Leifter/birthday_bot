# Скрипт для сремблирования данных в базах данных эмулятора

from telegram_chat import *
from telegram_user import *
import random

from Emulator.telegram_emu import TelegramClient, ErrorNoGroupFound


def get_hex_digit(num, tetr_num):
    if tetr_num > 7:
        raise Exception("get_hex_digit: tetrad number more then 7")
    return (num >> (tetr_num * 4)) & 0xF


def change_hex_digit(num, tetr, tetr_num):
    if tetr_num > 7:
        raise Exception("change_hex_digit: tetrad number more then 7")
    if tetr < 0 or tetr > 0xF:
        raise Exception("change_hex_digit: tetr < 0 or tetr > 0xF")
    mask = ((~(0xF << (tetr_num * 4))) & 0xFFFFFFFF)
    num = num & mask
    return num | (tetr << (tetr_num * 4))


def get_scramble_num(num):
    rand1 = random.randint(0,7)
    while True:
        rand2 = random.randint(0,7)
        if rand1 != rand2:
            break
    tetr1 = get_hex_digit(num, rand1)
    tetr2 = get_hex_digit(num, rand2)
    num = change_hex_digit(num, tetr1, rand2)
    num = change_hex_digit(num, tetr2, rand1)
    return num


def get_collapsed_num(num):
    num = get_scramble_num(num)
    num >>= 4
    return num


def get_scramble_ids(clinet):
    participants = client.participants
    part_ids = [u.id for u in participants]
    scramble_dict = {}
    for id in part_ids:
        scramble_dict[id] = get_collapsed_num(id)
    return scramble_dict


client = TelegramClient("scramble", 123456, "zzzzzzzzzzzzzzzzzzzzzzz", proxy=None)  # создаем объект для работы с Телеграмом


def test_get_scramble_num():
    nums = [0xABCDEF01, 0x12345678, 0x32457841, 0xBABADEDA]
    for n in nums:
        print("{:08X} -> {:08X}".format(n, get_scramble_num(n)))


scramble_ids = get_scramble_ids(client)
# Меняем id пользователей
for part in client.participants:
    part.id = scramble_ids[part.id]

for dialog in client.dialogs:
    parts_ids_scramble = []
    for part_id in dialog.participants_ids:
        parts_ids_scramble.append(scramble_ids[part_id])

    dialog.participants_ids = parts_ids_scramble

TelegramUser.save_employees_to_json("users.json", client.participants)
TelegramChat.save_dialogs_to_json("dialogs.json", client.dialogs)

print("Some")
test_get_scramble_num()
