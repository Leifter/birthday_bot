## 1. Что это?
Бот, создающий группу с днями рождения. Именинник в группу не приглашается, за исключением случая, когда Бот работает с его аккаунта.
(Не получается запускать два бота одновременно. Возможно нужно менять session_name?). Проверено на Python 3.7 x64. Бот может исполняться только от лица реального пользователся с зарегистрированным номером телефона. Бот позволяет работать в неактивном режиме, когда он не будет создавать новых групп и в активном режиме с полным функционалом.
Настройки бота хранятся в config.py, как питоновские переменные. Содержание файла конфигурации следующее:
```python
hour_to_check_start = 10           # Начало временного интервала, когда бот работает в активном режиме
hour_to_check_end = 18             # Конец временного интервала, когда бот работает в активном режиме
delay_in_days = 7                  # За сколько дней до дня рождения создавать группу
margin_in_days = 3                 # FIXME. Зарезервированно для объединения дней рождения, расположенных рядом
employees_file = "data/emps.json"  # Файл с данными о сотрудниках
debug_id = 12345678                # id группы или пользователя куда будет сыпаться отладочная информация
chats_filter = [...]               # Список ИД групп, от которых бот принимает интерактивные команды
common_group_id = 22222222         # id группы, в которой кучкуются весь круг людей, которых эти дни рождения касаются (общая группа)

proxy = proxies.inner_proxy()                  # Данные по прокси-серверу. Если не нужен, то None
session_name = "birthday_bot"                  # Телеграмовский реквизит. ?Произвольное имя сессии? 
api_id = 1111111                               # Телеграмовский реквизит. Выдается при создании приложения в аккаунте телеграма 
api_hash = "794b1e05e14a99c66d009a4bacb072cс"  # Телеграмовский реквизит. Выдается при создании приложения в аккаунте телеграма 
```

## 2. Формат юнита базы данных, храниться в файле employees_file в формате json:
```python
    {
        "id": 12345678,  # id пользователя. Можно узнать с помощью bd_bot get_chat_member_id, либо оно будет получено при bd_bot update_user_data из группы с common_group_id. Если человек не в Телеге, то null
        "num": 23,       # Не значимо, просто порядковый номер
        "b_stat": 1,     # Это для тех, кто не участвует в этом в сем по тем или иным причинам (если 0), но его данные зачем-то нужно хранить. Можно использовать при тестировании, что бы всех не тревожить. 0-пользователь не учитывается, 1-учитывается
        "name": "Иван",                # Заполняется вручную. Имя 
        "surname": "Иванов",           # Заполняется вручную. Фамилия
        "patronymic": "Иванович",      # Заполняется вручную. Отчество
        "b_date": "29-02",             # День рождения, может быть в формате "дд-мм-гггг" или "дд-мм"
        "phone": "79165555555",        # Берется из телеграма. Телефон, эти данные берутся из телеги, или null
        "b_group_id": 0,               # Содержит id созданной группы
        "gender": null,                # Пока не используется. Нужно для правильного склонения имен by Petrovich. Но что-то пошло не так. Все имена бот применяет в именительно падеже
        "first_name": "ИванРабота",    # Берется из телеграма. Имя
        "last_name": null,             # Берется из телеграма. Фамилия
        "username": "ivan_ivanov",     # Берется из телеграма. Ник
        "isTelegramData": true         # Есть ли данные по пользователю, полученные из телеграма. FIXME Лучше не трогать, кажется ни на что не влияет
    },
```

## 3. Интерактивные возможности (масштабируются в commands.py)
```
Получить справку: bd_bot help
Получить привет от бота: bd_bot reply
Показать данные по дням рождения: bd_bot show_bd
Получить ID группы (dialog_limit, количество искомых диалогов при поиске. Поиск начинается с самых свежих): bd_bot get_group_id {"group_name": "group name", "dialog_limit": 50}
Получить из участника группы (все данные пользователя указывать не обязательно): bd_bot get_chat_member_id {"group_name": "group name", "username": "name", "phone": 8911111, "first_name": "imya", "last_name": "familiya", "dialog_limit": 50}
Обновить данные по пользователям общей группы в базе данных: bd_bot update_user_data
Получить телеграмовский объект по ID (сообщение, юзверя, чат и т.п): bd_bot get_entity_by_id {"id": 1234567}
Повторно подгрузить данные по пользователям из файла: bd_bot reload_bd_data
```

## 4. Адаптация под себя
 - Зарегистрировать приложение на https://my.telegram.org (читать тут https://core.telegram.org/api/obtaining_api_id). На выходе получим api_id и api_hash
 -- Зайти в аккаунт
 -- Далее API development tools
 -- В окне Create new application: Заполнить соответствующие поля и получить api_id, api_hash для нового Телеграм-приложения
 - Изменить api_id и api_hash и прочие настройки в файле data/config.py
 - Убедиться в отсутствии предыдущего .session - файла. Иначе бот будет работать на предыдущей сессии. Удалить его если таковой уже был
 - Установить proxy-сервер в data/config.py и data/proxies.py
 - Запустить бота, находясь в его директории, через python main.py
 - Ввести номер телефона и, далее, присланный код подтверждения
 - Запустить в неактивном режиме. Для этого при старте бота не вводить слово aсtivate, введя любое другое
 - Проверить работу бота отправив ему сообщение bd_bot, должен вернуться хелп по интерактивным командам
 - Определить ID общей группы, откуда будет сформирована "рыба" базы данных через bd_bot get_group_id {"group_name": "group name", "dialog_limit": 50}. (?Бот должен быть членом группы?)
 - Выключить бота через Ctrl+C etc. Указать ID общей группы в config/common_group_id
 - Перезагрузить бота так же в неактивном режиме
 - При перезагрузке бот должен получить данные по пользователям из общей группы. Сохранить базу данных bd_bot update_user_data
 - Отредактировать вручную недостающие параметры в базе данных пользователей в файле БД data/emps.json (см п.5)
 - Подгрузить отредактированные данные через bd_bot reload_bd_data. (Файл базы данных и конфигурации бота рекомендуется хранить в отдельном приватном репозитории)
 - Перезагрузить бота, теперь уже можно в активном режиме

## 5. Для изменения базы данных, если:
a) Нужно отменить или включить празднование ДР какого-либо человека:
- меняем в текстовом файле базы данных b_stat человека (0 - празднует/1 - не празднует), сохраняем
- выполняем интерактивную команду bd_bot reload_bd_data

б) Нужно добавить нового сотрудника в БД, если он только добавился в общую группу:
- определяем id пользователя через bd_bot get_chat_member_id
- копипастим нового сотрудника в текстовом файле БД и меняем его ID на определенный ранее, добавляем дату дня рождения, bd_stat и пр.
- подгружаем новую БД в память бота bd_bot reload_bd_data
- дополняем данные по сотруднику из общего чата и сортируем БД bd_bot update_user_data

## 6. Возможности по отладке
    6.1. Можно менять режимы отладки установкой переменных в birthday_bot.py
    PASSIVE_ONLY = False   # Для отладки пассивного режима только. Бот не совершает активных действий, как-то создание групп с днями рождений, а только взаимодействует в интерактивном режиме
    EMULATION = False      # Режим эмуляции. Связь с телеграмом эмулируется заглушками из /Emulator
    DEBUG_ID = None        # ID для отсылки в телеграмм отладочной информации (устанавливается из config.py)
    6.2 Можно формировать список групп в которых возможно интерактивное взаимодействие с ботом (см. data/config.py chats_filter)

## 7. Струтура проекта
```
/
│   birthday_bot.py                    # основной код
│   birthday_bot.session               # кэш сессии бота
│   bot_status.py                      # Класс, хранящий статус бота
│   commands.py                        # Модуль ответственный за интерактив   
│   get_days_to_birth_day.py           # Функция расчета
│   get_information.py                 # Модуль про получение данных из телеграма
│   main.py                            # Стартовый модуль, включает логгирование и перехват исключений
│   petrovich_hotfix.py                # Заплатка для Петрович. FIXME
│   readme.md                          # Этот файл
│   requirements.txt                   # Требуемые пакеты. Ставятся pip install -r requirements.txt
│   telegram_chat.py                   # Класс чата. Применяется при отладке
│   telegram_user.py                   # Класс пользователя
│   ToDo.lst
│   
├───data
│       config.py                      # Файл с конфигурацией бота (настраивается под себя)
│       emps.json                      # Файл с базой данных по именинникам
│       proxies.py                     # Прокси для подключения к Телеграму
│       
├───Emulator                # То что применяется для отладки. См EMULATOR в birthday_bot.py
│       asincio_test.py
│       bot_debug.py
│       datetime_emu.py
│       dialogs.json
│       emu_test.py
│       group_emu.py
│       message_emu.py
│       telegram_emu.py
│       users.json
│       __init__.py
│       
├───Logger                   # То, что отвечает за логгирование
│       free_space.py
│       install.py
│       logger.py
│       logger_test.py
│       logger_test_up.py
│       test_bench_loader.py
│       __init__.py
│       
├───packages                 # Требуемые пакеты
│       cffi-1.14.0-cp37-cp37m-win_amd64.whl
│       construct-2.10.56.tar.gz
│       cryptg-0.2.post0-cp37-cp37m-win_amd64.whl
│       install_all.bat
│       ipaddress-1.0.23-py2.py3-none-any.whl
│       Petrovich-1.0.0.tar.gz
│       pyaes-1.6.1.tar.gz
│       pyasn1-0.4.8-py2.py3-none-any.whl
│       pycparser-2.20-py2.py3-none-any.whl
│       PySocks-1.7.1-py3-none-any.whl
│       rsa-4.0-py2.py3-none-any.whl
│       six-1.14.0-py2.py3-none-any.whl
│       Telethon-1.11.3-py3-none-any.whl
│       transitions-0.8.1-py2.py3-none-any.whl
│       
└───tests                   # Тесты отладночные
        test_birthday_bot.py
        test_event.py
        test_from_birth_days_string.py
        test_get_days_to_birth_day.py
        test_petrovich.py
        __init__.py
```