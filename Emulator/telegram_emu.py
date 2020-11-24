# -*- coding: UTF-8 -*-
import typing
import asyncio
from Emulator import bot_debug
from telegram_user import TelegramUser
from telegram_chat import TelegramChat

import os

from telethon.tl import types
from telethon.events.common import EventBuilder, EventCommon

DEBUG_USERNAME = "stepan panin"

class ErrorNoGroupFound(Exception):
    pass

"""
class Loop:
    def __init__(self):
        print("Loop init")

    def run_until_complete(self):
    pass
"""

class TelegramClient:
    def __init__(
            self: 'TelegramClient',
            session: 'typing.Union[str, Session]',
            api_id: int,
            api_hash: str,
            *,
#            connection: 'typing.Type[Connection]' = ConnectionTcpFull,
#            use_ipv6: bool = False,
            proxy: typing.Union[tuple, dict] = None,
#            timeout: int = 10,
#            request_retries: int = 5,
#            connection_retries: int =5,
#            retry_delay: int = 1,
#            auto_reconnect: bool = True,
#            sequential_updates: bool = False,
#            flood_sleep_threshold: int = 60,
#            device_model: str = None,
#            system_version: str = None,
#            app_version: str = None,
#            lang_code: str = 'en',
#            system_lang_code: str = 'en',
            loop: asyncio.AbstractEventLoop = None):
#            base_logger: typing.Union[str, logging.Logger] = None):
        self.session = session
        self.api_id = api_id
        self.api_hash = api_hash
        self.proxy = proxy

        self._loop = asyncio.get_event_loop()

        #self.dialogs = [Dialog(1, "Болтанка Advanced"), Dialog(2, "Флэйм")]   # Список с доступными диалогами
        #self.participants = [Participant(1, "Вася"), Participant(2, "Коля")]  # Список участников диалога
        cur_script_dir = self.emu_def_get_cur_script_dir()

        self.dialogs = TelegramChat.load_dialogs_from_json(os.path.join(cur_script_dir, bot_debug.DIALOG_LST_JSON))
        self.participants = TelegramUser.load_employees_from_json(os.path.join(cur_script_dir, bot_debug.USER_LST_JSON))

        #self.loop = Loop()

    # метод, вызываемый с with
    def __enter__(self):
        #print("<Emulator> __enter__")
        return self

    # Метод после завершения with
    def __exit__(self, exc_type, exc_val, exc_tb):  #(self, type, value, traceback)
        pass
        #print(<Emulator> "__exit__")

    async def __call__(self: 'TelegramClient', request, ordered=False):
        print("<Emulator> Telegram Emu __call__")
        return await request.resolve(self, "utils_sub")

    def emu_def_get_cur_script_dir(self):
        cur_script_dir_list = __file__.split(os.sep)[:-1]
        drive_letter = cur_script_dir_list[0]
        cur_script_dir = cur_script_dir_list[1:]               # Путь к текущему скрипту списком, без C: иначе глючит
        cur_script_dir = os.path.join(drive_letter + os.sep, *cur_script_dir)  # Путь к текущему скрипту
        # print("<Emulator> " + cur_script_dir)
        return cur_script_dir

    def emu_def_get_participant_by_id(self, participant_id):
        participant = None
        for p in self.participants:  # Поиск диалога с нужным ID
            if p.id == participant_id:
                if participant:
                    raise Exception("<Emulator> В списке с участниками имеется 2 участника с ID {}".format(p))
                participant = p
        if not participant:
            raise Exception("<Emulator> В списке с участниками ID {} не обнаружен".format(participant_id))
        return participant


    # Метод эмулятора. Получить описатель диалога по id
    def emu_def_get_dialog_by_id(self, chat_id):
        dialog = None
        for d in self.dialogs:  # Поиск диалога с нужным ID
            if d.id == chat_id:
                if dialog:
                    raise ErrorNoGroupFound("<Emulator> В списке с диалогами имеется 2 диалога {}".format(d))
                dialog = d
        if not dialog:
            raise ErrorNoGroupFound("<Emulator> В списке с диалогами не обнаружен диалог с ID {}".format(chat_id))
        return dialog

    def emu_def_add_new_dialog(self, title, members):
        existing_ids = [d.id for d in self.dialogs]
        new_id = 100 # Определение нового ID
        while True:
            if new_id not in existing_ids:
                break
            new_id += 1

        members_names = ["{} {} {}".format(self.emu_def_get_participant_by_id(id).first_name,
                                           self.emu_def_get_participant_by_id(id).last_name,
                                           self.emu_def_get_participant_by_id(id).username,) for id in members]
        print("<Emulator> emu_def_add_new_dialog {}".format(members_names))

        new_chat = TelegramChat(new_id, title=title, participants_ids=members)
        self.dialogs.append(new_chat)
        cur_script_dir = self.emu_def_get_cur_script_dir()
        TelegramChat.save_dialogs_to_json(os.path.join(cur_script_dir, bot_debug.DIALOG_LST_JSON), self.dialogs) # Сохранить новый диалог в БД
        return new_chat

    # Метод эмулятора. Получить описатель диалога по его имени
    def emu_def_get_dialog_by_name(self, dialog_name):
        dialog = None
        for d in self.dialogs:  # Поиск диалога с нужным ID
            if d.title == dialog_name:
                if dialog:
                    raise Exception("<Emulator> В списке с диалогами имеется 2 диалога {}".format(d))
                dialog = d
        if not dialog:
            raise Exception("<Emulator> В списке с диалогами не обнаружен диалог с названием {}".format(dialog_name))
        return dialog


    async def get_participants(
            self: 'TelegramClient',
            *args,
            **kwargs) -> 'hints.TotalList':
        """
        Same as `iter_participants()`, but returns a
        `TotalList <telethon.helpers.TotalList>` instead.

        Example
            .. code-block:: python

                users = await client.get_participants(chat)
                print(users[0].first_name)

                for user in users:
                    if user.username is not None:
                        print(user.username)
        """
        #return await self.iter_participants(*args, **kwargs).collect()
        fut = self._loop.create_future() # Создаем Future заглушку
        #print('hello ...')
        #l = loop.run_until_complete(fut)
        chat_id = args[0]
        dialog = self.emu_def_get_dialog_by_id(chat_id)

        participants = []
        for p in self.participants: # Поиск пользователей данного чата
            if p.id in dialog.participants_ids:
                participants.append(p)

        fut.set_result(participants) # Future возвращает конктретный контент
        print("<Emulator> async def get_participants")
        print(self.participants)
        #return await self.iter_dialogs(*args, **kwargs).collect()
        return await fut

    async def get_dialogs(self: 'TelegramClient', *args, **kwargs) -> 'hints.TotalList':
        """
        Same as `iter_dialogs()`, but returns a
        `TotalList <telethon.helpers.TotalList>` instead.

        Example
            .. code-block:: python

                # Get all open conversation, print the title of the first
                dialogs = await client.get_dialogs()
                first = dialogs[0]
                print(first.title)

                # Use the dialog somewhere else
                await client.send_message(first, 'hi')

                # Getting only non-archived dialogs (both equivalent)
                non_archived = await client.get_dialogs(folder=0)
                non_archived = await client.get_dialogs(archived=False)

                # Getting only archived dialogs (both equivalent)
                archived = await client.get_dialogs(folder=1)
                non_archived = await client.get_dialogs(archived=True)
        """
        fut = self._loop.create_future() # Создаем Future заглушку
        print('<Emulator> get_dialogs')
        fut.set_result(self.dialogs) # Future возвращает конктретный контент
        #return await self.iter_dialogs(*args, **kwargs).collect()
        return await fut

    async def edit_permissions(
            self: 'TelegramClient',
            entity: 'hints.EntityLike',
            user: 'typing.Optional[hints.EntityLike]' = None,
            until_date: 'hints.DateLike' = None,
            *,
            view_messages: bool = True,
            send_messages: bool = True,
            send_media: bool = True,
            send_stickers: bool = True,
            send_gifs: bool = True,
            send_games: bool = True,
            send_inline: bool = True,
            send_polls: bool = True,
            change_info: bool = True,
            invite_users: bool = True,
            pin_messages: bool = True) -> types.Updates:
        fut = self._loop.create_future()  # Создаем Future заглушку
        print('<Emulator> edit_permissions_async')
        fut.set_result(True)  # Future возвращает конктретный контент
        return await fut

    def edit_permissions_sync(
            self: 'TelegramClient',
            entity: 'hints.EntityLike',
            user: 'typing.Optional[hints.EntityLike]' = None,
            until_date: 'hints.DateLike' = None,
            *,
            view_messages: bool = True,
            send_messages: bool = True,
            send_media: bool = True,
            send_stickers: bool = True,
            send_gifs: bool = True,
            send_games: bool = True,
            send_inline: bool = True,
            send_polls: bool = True,
            change_info: bool = True,
            invite_users: bool = True,
            pin_messages: bool = True) -> types.Updates:
        print("<Emulator> edit_permissions ID = {}, Title = {}".format(entity, self.emu_def_get_dialog_by_id(entity).title))
        return True

    async def send_message(
            self: 'TelegramClient',
            entity: 'hints.EntityLike',
            message: 'hints.MessageLike' = '',
            *,
            reply_to: 'typing.Union[int, types.Message]' = None,
            parse_mode: typing.Optional[str] = (),
            link_preview: bool = True,
            file: 'typing.Union[hints.FileLike, typing.Sequence[hints.FileLike]]' = None,
            force_document: bool = False,
            clear_draft: bool = False,
            buttons: 'hints.MarkupLike' = None,
            silent: bool = None,
            schedule: 'hints.DateLike' = None
    ) -> 'types.Message':
        """
        Sends a message to the specified user, chat or channel.

        The default parse mode is the same as the official applications
        (a custom flavour of markdown). ``**bold**, `code` or __italic__``
        are available. In addition you can send ``[links](https://example.com)``
        and ``[mentions](@username)`` (or using IDs like in the Bot API:
        ``[mention](tg://user?id=123456789)``) and ``pre`` blocks with three
        backticks.

        Sending a ``/start`` command with a parameter (like ``?start=data``)
        is also done through this method. Simply send ``'/start data'`` to
        the bot.

        See also `Message.respond() <telethon.tl.custom.message.Message.respond>`
        and `Message.reply() <telethon.tl.custom.message.Message.reply>`.

        Arguments
            entity (`entity`):
                To who will it be sent.

            message (`str` | `Message <telethon.tl.custom.message.Message>`):
                The message to be sent, or another message object to resend.

                The maximum length for a message is 35,000 bytes or 4,096
                characters. Longer messages will not be sliced automatically,
                and you should slice them manually if the text to send is
                longer than said length.

            reply_to (`int` | `Message <telethon.tl.custom.message.Message>`, optional):
                Whether to reply to a message or not. If an integer is provided,
                it should be the ID of the message that it should reply to.

            parse_mode (`object`, optional):
                See the `TelegramClient.parse_mode
                <telethon.client.messageparse.MessageParseMethods.parse_mode>`
                property for allowed values. Markdown parsing will be used by
                default.

            link_preview (`bool`, optional):
                Should the link preview be shown?

            file (`file`, optional):
                Sends a message with a file attached (e.g. a photo,
                video, audio or document). The ``message`` may be empty.

            force_document (`bool`, optional):
                Whether to send the given file as a document or not.

            clear_draft (`bool`, optional):
                Whether the existing draft should be cleared or not.
                Has no effect when sending a file.

            buttons (`list`, `custom.Button <telethon.tl.custom.button.Button>`, :tl:`KeyboardButton`):
                The matrix (list of lists), row list or button to be shown
                after sending the message. This parameter will only work if
                you have signed in as a bot. You can also pass your own
                :tl:`ReplyMarkup` here.

                All the following limits apply together:

                * There can be 100 buttons at most (any more are ignored).
                * There can be 8 buttons per row at most (more are ignored).
                * The maximum callback data per button is 64 bytes.
                * The maximum data that can be embedded in total is just
                  over 4KB, shared between inline callback data and text.

            silent (`bool`, optional):
                Whether the message should notify people in a broadcast
                channel or not. Defaults to `False`, which means it will
                notify them. Set it to `True` to alter this behaviour.

            schedule (`hints.DateLike`, optional):
                If set, the message won't send immediately, and instead
                it will be scheduled to be automatically sent at a later
                time.

        Returns
            The sent `custom.Message <telethon.tl.custom.message.Message>`.

        Example
            .. code-block:: python

                # Markdown is the default
                await client.send_message('lonami', 'Thanks for the **Telethon** library!')

                # Default to another parse mode
                client.parse_mode = 'html'

                await client.send_message('me', 'Some <b>bold</b> and <i>italic</i> text')
                await client.send_message('me', 'An <a href="https://example.com">URL</a>')
                # code and pre tags also work, but those break the documentation :)
                await client.send_message('me', '<a href="tg://user?id=me">Mentions</a>')

                # Explicit parse mode
                # No parse mode by default
                client.parse_mode = None

                # ...but here I want markdown
                await client.send_message('me', 'Hello, **world**!', parse_mode='md')

                # ...and here I need HTML
                await client.send_message('me', 'Hello, <i>world</i>!', parse_mode='html')

                # If you logged in as a bot account, you can send buttons
                from telethon import events, Button

                @client.on(events.CallbackQuery)
                async def callback(event):
                    await event.edit('Thank you for clicking {}!'.format(event.data))

                # Single inline button
                await client.send_message(chat, 'A single button, with "clk1" as data',
                                          buttons=Button.inline('Click me', b'clk1'))

                # Matrix of inline buttons
                await client.send_message(chat, 'Pick one from this grid', buttons=[
                    [Button.inline('Left'), Button.inline('Right')],
                    [Button.url('Check this site!', 'https://lonamiwebs.github.io')]
                ])

                # Reply keyboard
                await client.send_message(chat, 'Welcome', buttons=[
                    Button.text('Thanks!', resize=True, single_use=True),
                    Button.request_phone('Send phone'),
                    Button.request_location('Send location')
                ])

                # Forcing replies or clearing buttons.
                await client.send_message(chat, 'Reply to me', buttons=Button.force_reply())
                await client.send_message(chat, 'Bye Keyboard!', buttons=Button.clear())

                # Scheduling a message to be sent after 5 minutes
                from datetime import timedelta
                await client.send_message(chat, 'Hi, future!', schedule=timedelta(minutes=5))
        """
        if type(entity) == type(int()):
            chat_id = entity
        else:
            raise Exception("<Emulator> Не реализован такой тип entity")
        dialog = self.emu_def_get_dialog_by_id(chat_id)     # Получить диалог по его ID
        print("<Emulator> send_message: Диалогу {} передано сообщение \"{}\"".format(dialog.title, message))

        fut = self._loop.create_future()  # Создаем Future заглушку
        fut.set_result(None)  # Future возвращает конктретный контент
        return await fut

    # Получить ID себя
    async def get_me(self):
        fut = self._loop.create_future()  # Создаем Future заглушку
        fut.set_result(self.emu_def_get_dialog_by_name(DEBUG_USERNAME).id)  # Future возвращает конктретный контент
        return await fut

    # Это из updates.py : UpdateMethods
    def on(self: 'TelegramClient', event: EventBuilder):
        """
        Decorator used to `add_event_handler` more conveniently.


        Arguments
            event (`_EventBuilder` | `type`):
                The event builder class or instance to be used,
                for instance ``events.NewMessage``.

        Example
            .. code-block:: python

                from telethon import TelegramClient, events
                client = TelegramClient(...)

                # Here we use client.on
                @client.on(events.NewMessage)
                async def handler(event):
                    ...
        """
        def decorator(f):
            self.add_event_handler(f, event)
            return f

        return decorator

    def add_event_handler(
            self: 'TelegramClient',
            callback: callable,
            event: EventBuilder = None):
        print("add_event_handler")

    # region Properties

    @property
    def loop(self: 'TelegramClient') -> asyncio.AbstractEventLoop:
        """
        Property with the ``asyncio`` event loop used by this client.

        Example
            .. code-block:: python

                # Download media in the background
                task = client.loop_create_task(message.download_media())

                # Do some work
                ...

                # Join the task (wait for it to complete)
                await task
        """
        return self._loop


    def __repr__(self):
        return "<Emulator> {} {} {} {}".format(self.session, self.api_id, self.api_hash, self.proxy)

print("<Emulator> Import telegram_emu")