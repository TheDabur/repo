# -*- coding: utf-8 -*-

"""
    TheDabur Add-on
    Copyright (C) 2017 TheDabur
"""

from os import path, makedirs
import json
import control
import time

CONFIG_JSON_FILE = "config.json"
CONFIG_NEXT_UPDATE_INTERVAL = 172800  # 2 days

class config:
    def __init__(self):
        try:
            makedirs(control.dataPath)
        except OSError:
            pass

        self.conf_file = path.join(control.dataPath, CONFIG_JSON_FILE)
        try:
            with open(self.conf_file, 'r') as f:
                self.conf = json.load(f)
        except:
            self.conf = {"version": "None", "updated_at": int(time.time()), "update_next_check": (int(time.time()) + CONFIG_NEXT_UPDATE_INTERVAL), "package": "None", "addons": []}
            self.save()

    def get(self):
        return self.conf

    def set(self, conf):
        self.conf = conf

    def save(self):
        with open(self.conf_file, 'w+') as f:
            json.dump(self.conf, f)

    def getVersion(self):
        try:
            return self.conf['version']
        except:
            return None

    def getUpdatedAt(self):
        try:
            return self.conf['updated_at']
        except:
            return None

    def getUpdateNextCheck(self):
        try:
            return self.conf['update_next_check']
        except:
            return None

    def getPackage(self):
        try:
            return self.conf['package']
        except:
            return None

    def getAddons(self):
        try:
            return set(self.conf['addons'])
        except:
            return []
