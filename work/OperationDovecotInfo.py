#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

class OperationDovecotHelper():

    def __init__(self,mail_user,da_ip):
        self.mail_user = mail_user
        self.da_ip = da_ip

    def get_user_quota(self):
        cmd = '/home/mail/dovecot/bin/doveadm quota get -u %s'%(self.mail_user)
        cmd2 = 'ansible %s -S -m shell -a'%(self.da_ip)
        cmd = cmd2+" '"+cmd+"'"
        return os.popen(cmd).readlines()

    def recalc_user_quota(self):
        cmd = '/home/mail/dovecot/bin/doveadm quota recalc -u %s' % (self.mail_user)
        cmd2 = 'ansible %s -S -m shell -a' % (self.da_ip)
        cmd = cmd2 + " '" + cmd + "'"
        return os.popen(cmd).readlines()

    def reload_dovecot(self):
        cmd = '/home/mail/dovecot/sbin/dovecot reload'
        cmd2 = 'ansible %s -S -m shell -a' % (self.da_ip)
        cmd = cmd2 + " '" + cmd + "'"
        return os.popen(cmd).readlines()