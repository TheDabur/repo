# -*- coding: utf-8 -*-

"""
    TheDabur Add-on
    Copyright (C) 2017 TheDabur
"""

import sys
from json import loads
from urllib2 import urlopen
from random import randint

sysaddon = sys.argv[0]


class packages:
    def __init__(self):
        self.pack_url = 'https://raw.githubusercontent.com/TheDabur/packages/master/packages.json?tkn={0}'.format(
            randint(0, 9223372036854775807))
        json_data = urlopen(self.pack_url)
        self.data = loads(json_data.read())

    def list(self):
        return self.data['packages']

    def get(self, package_id):
        for package in self.list():
            if package['id'] == package_id:
                return package
        return False

    def exists(self, package_id):
        if self.get(package_id):
            return True
        else:
            return False

    def getVersion(self):
        return self.data['version']
