# -*- coding: UTF-8 -*-
import json

class TelegramChat:
    def __init__(self, id, **kwargs):
        self.id = id
        self.title = kwargs.get("title")
        self.participants_ids = kwargs.get("participants_ids")

    def __repr__(self):
        return f"TelegramChat({self.id}: {self.title})"

    def asdict(self):
        return {
            "id" : self.id,
            "title": self.title,
            "participants_ids": self.participants_ids,
        }

    @staticmethod
    def save_dialogs_to_json(filename, dialogs, encoding='utf8'):
        i = 1
        with open(filename, 'w', encoding=encoding) as f:
            print(dialogs)
            json.dump([e.asdict() for e in dialogs], f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_dialogs_from_json(filename, encoding='utf8'):
        dialogs = list()
        with open(filename, 'r', encoding=encoding) as f_json:
            for d in json.load(f_json):
                dialogs.append(TelegramChat(**d))
        return dialogs

