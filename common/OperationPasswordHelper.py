#!/usr/bin/python3
#coding=utf-8

import hashlib

class EncryptionHelper():
    def __init__(self,string_need_to_encrypt):
        self.string_need_to_encrypt = string_need_to_encrypt

    def genearteMD5(self):
        hl = hashlib.md5()
        hl.update(self.string_need_to_encrypt.encode(encoding='utf-8'))
        return hl.hexdigest()