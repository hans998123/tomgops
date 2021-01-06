#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

class LogggerHelper():
    """自定日志之类"""
    def __init__(self, level):
        self.level = level

    def my_log(self,name):
        # 创建自己的日志收集器
        my_log = logging.getLogger(name)
        my_log.setLevel(self.level.upper())
        # 创建一个日志输出渠道（输出到控制台）
        handler1 = logging.StreamHandler()
        handler1.setLevel(self.level.upper())
        # 创建一个日志输出渠道（输出到文件）
        handler2 = logging.FileHandler('migrate.log', encoding='utf8')
        handler2.setLevel(self.level.upper())
        # 将输出渠道添加到日志收集器中
        my_log.addHandler(handler1)
        my_log.addHandler(handler2)
        # 设置日志输出的格式
        formatter = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        ft1 = logging.Formatter(formatter)
        # 设置日志输出的格式
        handler1.setFormatter(ft1)
        handler2.setFormatter(ft1)
        return my_log