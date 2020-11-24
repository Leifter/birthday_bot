# -*- coding: UTF-8 -*-
from telethon.tl.tlobject import TLRequest
from typing import Optional, List, Union, TYPE_CHECKING
import struct
from Emulator.group_emu import Group


class CreateChatRequest(TLRequest):
    CONSTRUCTOR_ID = 0x9cb126e
    SUBCLASS_OF_ID = 0x8af52aac

    def __init__(self, users: List['TypeInputUser'], title: str):
        """
        :returns Updates: Instance of either UpdatesTooLong, UpdateShortMessage, UpdateShortChatMessage, UpdateShort, UpdatesCombined, Updates, UpdateShortSentMessage.
        """
        self.users = users
        self.title = title
        print("<Emulator> CreateChatRequest: __init__, self.title {}, self.users = users {}".format(self.title,self.users))

    async def resolve(self, client, utils):
        print("<Emulator> CreateChatRequest resolve")
        new_chat = client.emu_def_add_new_dialog(title=self.title, members=self.users)
        '''
        _tmp = []
        for _x in self.users:
            _tmp.append(utils.get_input_user(await client.get_input_entity(_x)))

        self.users = _tmp
        '''
        # group.chats[0].id
        group = Group([new_chat])  # Создаем новую группу?
        return group

    def to_dict(self):
        return {
            '_': 'CreateChatRequest',
            'users': [] if self.users is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.users],
            'title': self.title
        }

    def __bytes__(self):
        return b''.join((
            b'n\x12\xcb\t',
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.users)),b''.join(bytes(x) for x in self.users),
            self.serialize_bytes(self.title),
        ))

    @classmethod
    def from_reader(cls, reader):
        reader.read_int()
        _users = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _users.append(_x)

        _title = reader.tgread_string()
        return cls(users=_users, title=_title)