#!/usr/bin/python3
#coding=utf-8

from common.ParamikoHelper import ParamikoHelper

class AntiSpamHelper():

    def __init__(self,hostname,username,port,private_key):
        self.hostname = hostname
        self.username = username
        self.port = port
        self.private_key = private_key

    @staticmethod
    def add_postscreen_access(sender_ip,status):
        res = sender_ip+" "+status
        with open('/root/paramiko_files/postscreen_access.cidr','a') as file_object:
            file_object.write(res+'\n')

    def add_barracuda_whitelist(self,local_path,remote_path):
        paramiko = ParamikoHelper(self.hostname,self.username,self.port,self.private_key)
        paramiko.sftp_upload_file(local_path,remote_path)
        paramiko.execute_command('postmap /etc/postfix/postscreen_access.cidr')
        paramiko.execute_command('/etc/init.d/postfix reload')