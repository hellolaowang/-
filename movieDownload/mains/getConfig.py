# -*- coding: utf-8 -*-
import os
import configparser

# 获取配置文件
configDir = os.path.dirname(os.path.dirname(__file__))
configFile = os.path.join(configDir, "config\config.ini")
# 定义一个配置文件对象
configPar = configparser.ConfigParser()
configPar.read(configFile, encoding="gb18030")

# 获取配置文件内容
m3u8FilePath = configPar.get("m3u8FilePath", "m3u8FilePath")
filePath = configPar.get("filePath", "filePath")
timeOut = configPar.get("timeOut", "timeOut")
postFix = configPar.get("postFix", "postFix")
