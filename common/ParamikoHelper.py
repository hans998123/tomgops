#!/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko

class SSHClient(object):
    def __init__(self, hostname, username,port,private_key):#我这是私钥登录,密码的话就写password
        self.hostname = hostname
        self.username = username
        self.port = port
        #self.password = password
        self.private_key = private_key
        self.ssh = None
        self._connect()

    def __del__(self):
        self.ssh.close()

    def _connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #self.ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
        self.ssh.connect(hostname=self.hostname,port=int(self.port),username=self.username,pkey=self.private_key)

    def execute_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        stdout = stdout.read().decode("utf-8")#这个得看你的服务器,有可能是gbk
        stderr = stderr.read().decode("utf-8")
        return stdout, stderr

    def sftp_upload_file(self,local_path,remote_path):
        sftp = self.ssh.open_sftp()
        sftp.put(local_path,remote_path)

    def sftp_download_file(self,local_path,remote_path):
        sftp = self.ssh.open_sftp()
        sftp.get(local_path,remote_path)