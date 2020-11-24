# -*- coding: UTF-8 -*-


# Глобальный объект со статусом бота
class BotStatus:
    def __init__(self):
        self.bd_loop_enable = False
        self.exception_occurred = 0

    def new_exception(self):
        self.exception_occurred += 1

    def set_bd_loop_status(self, enable):
        self.bd_loop_enable = enable

    def bd_loop_new_exception(self):
        self.set_bd_loop_status(False)
        self.new_exception()

    def __repr__(self):
        return "Bot status: bd_loop_enable: {}, exception_occurred: {}".format(self.bd_loop_enable, self.exception_occurred)


BOT_STATUS = BotStatus()   # Глобальный объект со статусом бота

if __name__ == "__main__":
    bot_status = BotStatus()
    bot_status.set_bd_loop_status(True)
    print(bot_status)
    bot_status.new_exception()
    bot_status.new_exception()
    bot_status.new_exception()
    print(bot_status)
    bot_status.bd_loop_new_exception()
    print(bot_status)
