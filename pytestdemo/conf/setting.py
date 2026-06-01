import os
import sys
import logging

DIR_PATH = os.path.dirname(os.path.dirname(__file__))
# print(DIR_PATH)

sys.path.append(DIR_PATH)           # 放到环境变量里去

# log日志的输出级别
LOG_LEVEL = logging.DEBUG           # 日志输出到文件的级别
STREAM_LOG_LEVEL = logging.DEBUG    # 输出日志到控制台的级别

# 文件路径
FILE_PATH = {
    'extract': os.path.join(DIR_PATH, 'extract.yaml')    # 连接跟目录和文件名
}

# print(FILE_PATH['extract'])