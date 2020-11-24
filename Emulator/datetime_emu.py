# -*- coding: UTF-8 -*-
from datetime import datetime as dt_origin
from datetime import *


datetime_start = dt_origin(year=2012, month=1, day=1, hour=1, minute=1, second=1)  # Начальнвй день
datetime_now = datetime_start


class datetime(dt_origin):

    def __new__(cls, *args, **kwargs):
        return dt_origin.__new__(dt_origin, *args, **kwargs)

    @classmethod
    def get_model_date(cls):
        global datetime_now
        # datetime_now += timedelta(days=1)
        print(datetime_now)
        datetime_now += timedelta(hours=4)
        return datetime_now

    @classmethod
    def now(cls):
        return cls.get_model_date()


if __name__ == "__main__":

    for i in range(100):
        print("{}".format(datetime.now()))


