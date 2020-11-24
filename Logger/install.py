#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import site
import shutil

TARGET_NAME = 'logger.py'

#print(sys.version_info)
#Проверка версии Python
if sys.version_info <= (2, 7):
	print('Error Python version too old sys.version_info <= (2, 7)')
	quit(1)

#Копирование собранной библиотеки в стандартную для питоновских модулей папку
sitePaths = site.getsitepackages()
installPath = sitePaths[0]

print(installPath)
print(TARGET_NAME, installPath + os.sep + TARGET_NAME)
shutil.copy(TARGET_NAME, installPath + os.sep + TARGET_NAME)   # копировать

quit(0)


