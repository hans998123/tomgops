#!/usr/bin/python3
#coding=utf-8

from common.ParamikoHelper import ParamikoHelper

class AntiSpamHelper():

    def __init__(self,sender,hostname,username,port,private_key):
        self.sender = sender
        self.hostname = hostname
        self.username = username
        self.port = port
        self.private_key = private_key