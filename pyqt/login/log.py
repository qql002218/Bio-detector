#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time


class LogFile:
    """
    自动化归档 ：
    为每一天的实验操作建立一个文件夹，其中包括但不局限于 logfile + 原视频 + 处理的视频 + 实验报告
    """

    def __init__(self):

        self.time = time.strftime("%Y-%m-%d", time.localtime())
        self.path = '/home/qiao/PycharmProjects/PythonLearning/LogFile/{time}'.format(time=self.time)
        self.create_dir_not_exist()
        self.create_logfile_not_exist()

    def create_dir_not_exist(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def create_logfile_not_exist(self):
        self.log_file = os.path.join(self.path, '{}.txt'.format(self.time))
        # print(self.log_file)
        if not os.path.exists(self.log_file):
            os.system("touch {}".format(self.log_file))  # 如果不存在这个文件，就自动创建一个

    def getLogFile(self):
        return self.log_file


if __name__ == '__main__':
    test = LogFile()
