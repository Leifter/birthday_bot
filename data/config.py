# -*- coding: UTF-8 -*-
from data import proxies
# день рождения будет проверяться в 10 часов дня
hour_to_check_start = 10
hour_to_check_end = 18
# время создание беседы, дней до др
delay_in_days = 9
# delay_in_days = 14
# за какой период времени объединять дни рождения
margin_in_days = 3
# файл с данными о сотрудниках
employees_file = "data/emps.json"
#employees_file = "boltalka.json"

debug_id = 12345678  # id группы или пользователя куда будет сыпаться отладочная информация
# id группы со всеми участниками, из которой будет создаваться новая

# Реципиенты
boltalka_id = -100138975694    # ID группы Болталка
big_test_id = 1213879100       # ID группы Бигтест
bd_bot_group_id = -31790909    # ID группы BD_BOT
me_id = 'me'                   # Собственный ID
chats_filter = [me_id, big_test_id, bd_bot_group_id, debug_id]  # От кого бот будет получать запросы

common_group_id = None     # ID общий группы. None для первого запуска

# proxy = proxies.outer_proxy()
proxy = proxies.inner_proxy() # Получить внутренний проксисервер

session_name = "birthday_bot"
# При изменении api_id и api_hash нужно удалять файл сессии
# Для получени реквизитов и работы с приложениями https://my.telegram.org/apps
api_id = 1111111
api_hash = "794b1e05e14a99c66d009a4bacb072cс"
