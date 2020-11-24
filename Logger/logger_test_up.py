# -*- coding:utf-8 -*-
import sys
import os
print("LoggerUP")
import logger

#newLogger = logger.Logger("some file")

import logger_test

print("LoggerUP: asdsdsda")
print("LoggerUP: <Error>lalalala")
print("LoggerUP: <Warning>la2dsfdsflalala")
print("LoggerUP: <Warning><Error>la2dsfdsflalala")
#print(sys.modules[__name__])
print(__name__)
print(os.path.basename(__file__))
#newLogger.closeLogger()