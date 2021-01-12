#!/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko

class ParamikoHelper():
    def __init__(self, hostname,username,port,private_key):#我这是私钥登录,密码的话就写password
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
        stdout = stdout.read().decode("utf-8")  # 这个得看你的服务器,有可能是gbk
        stderr = stdout.read().decode("utf-8")  # 这个得看你的服务器,有可能是gbk
        return stdout, stderr

    def sftp_upload_file(self,local_path,remote_path):
        sftp = self.ssh.open_sftp()
        sftp.put(local_path,remote_path)

    def sftp_download_file(self,remote_path,local_path):
        sftp = self.ssh.open_sftp()
        sftp.get(remote_path,local_path)

    def mkdir(self,target_path,mode='0644'):
        sftp = self.ssh.open_sftp()
        sftp.mkdir(target_path, mode)

    def rmdir(self,target_path):
        sftp = self.ssh.open_sftp()
        sftp.rmdir(target_path)

    def listdir(self, target_path):
        sftp = self.ssh.open_sftp()
        return sftp.listdir(target_path)

    def remove(self, target_path):
        sftp = self.ssh.open_sftp()
        sftp.remove(target_path)

    def listdirattr(self,target_path):
        try:
            sftp = self.ssh.open_sftp()
            list = sftp.listdir_attr(target_path)
            return list
        except BaseException as e:
            return e

    def stat(self, remote_path):
        sftp = self.ssh.open_sftp()
        return sftp.stat(remote_path)