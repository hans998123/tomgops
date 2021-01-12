#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

class OperationHelper():

    def __init__(self,mail_user,da_ip,new_da_ip,dict_da_path,mail_file):
        self.mail_user = mail_user
        self.da_ip = da_ip
        self.new_da_ip = new_da_ip
        self.dict_da_path = dict_da_path
        self.mail_file = mail_file

    def compress(self):
        cmd2 = "cd " + self.dict_da_path + " && tar -zcvf " + self.mail_user + ".tar.gz *"
        cmd = "ansible " + self.da_ip + " -S -m shell -a '" + cmd2 + "'"
        res = os.popen(cmd).readlines()
        return res

    def create_http(self):
        cmd2 = "cd " + self.dict_da_path + " && nohup python -m SimpleHTTPServer </dev/null >/dev/null 2>&1 &"
        cmd = "ansible " + self.da_ip + " -S -m shell -a '" + cmd2 + "'"
        res = os.popen(cmd).readlines()
        return res

    def kill_http_server(self):
        if self.dict_da_path == '172.25.16.231':
            cmd2 = "ps -ef | grep SimpleHTTPServer | grep -v grep | cut -c 9-15 |xargs kill -9"
            cmd = "ansible " + self.da_ip + " -m shell -a '" + cmd2 + "'"
            res = os.popen(cmd).readlines()
            return res
        else:
            cmd2 = "ps -ef | grep SimpleHTTPServer | grep -v grep | cut -c 9-15 |xargs kill -9"
            cmd = "ansible " + self.da_ip + " -S -m shell -a '" + cmd2 + "'"
            res = os.popen(cmd).readlines()
            return res

    def make_path(self):
        if self.new_da_ip == '172.25.16.231':
            cmd2 = "mkdir -p " + self.dict_da_path + " && chown -R vmail:vmail " + self.dict_da_path
            cmd = "ansible " + self.new_da_ip + " -m shell -a '" + cmd2 + "'"
            res = os.popen(cmd).readlines()
            return res
        else:
            cmd2 = "mkdir -p " + self.dict_da_path + " && chown -R vmail:vmail " + self.dict_da_path
            cmd = "ansible " + self.new_da_ip + " -S -m shell -a '" + cmd2 + "'"
            res = os.popen(cmd).readlines()
            return res

    def download_file(self):
        if self.new_da_ip == '172.25.16.231':
            cmd2 = "cd " + self.dict_da_path + " && wget http://" + self.da_ip + ":8000/" + self.mail_user + ".tar.gz"
            cmd = "ansible " + self.new_da_ip + " -m shell -a '" + cmd2 + "'"
            res = os.popen(cmd).readlines()
            return res
        else:
            cmd2 = "cd " + self.dict_da_path + " && wget http://" + self.da_ip + ":8000/" + self.mail_user + ".tar.gz"
            cmd = "ansible " + self.new_da_ip + " -S -m shell -a '" + cmd2 + "'"
            res = os.popen(cmd).readlines()
            return res

    def decompress(self):
        if self.new_da_ip == '172.25.16.231':
            cmd2 = "cd " + self.dict_da_path + " && tar -zxvf " + self.mail_user + ".tar.gz"
            cmd = "ansible " + self.new_da_ip + " -m shell -a '" + cmd2 + "'"
            res = os.popen(cmd).readlines()
            return res
        else:
            cmd2 = "cd " + self.dict_da_path + " && tar -zxvf " + self.mail_user + ".tar.gz"
            cmd = "ansible " + self.new_da_ip + " -S -m shell -a '" + cmd2 + "'"
            res = os.popen(cmd).readlines()
            return res

    def reload_mail(self):
        if self.new_da_ip == '172.25.16.231':
            cmd2 = '/home/mail/dovecot/sbin/dovecot reload'
            cmd = "ansible " + self.new_da_ip + " -m shell -a '" + cmd2 + "'"
            res = os.popen(cmd).readlines()
            return res
        else:
            cmd2 = '/home/mail/dovecot/sbin/dovecot reload'
            cmd = "ansible " + self.new_da_ip + " -S -m shell -a '" + cmd2 + "'"
            res = os.popen(cmd).readlines()
            return res