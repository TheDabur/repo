# -*- coding: utf-8 -*-

"""
    TheDabur Add-on
    Copyright (C) 2017 TheDabur
"""

import sys
from urllib2 import URLError

import packages

import control

sysaddon = sys.argv[0]


class menu:

    def __init__(self):
        pass

    def root(self):
        try:
            lang = control.infoLabel('System.Language')
            for package in packages.packages().list():
                try:
                    name = package['name'][lang]
                except:
                    try:
                        name = package['name']['English']
                    except:
                        name = package['name']
                try:
                    desc = package['description'][lang]
                except:
                    try:
                        desc = package['description']['English']
                    except:
                        desc = package['description']

                self.addDirectoryItem(name, package['id'], 'download', '', '', desc)

        except URLError, e:
            control.dialog.ok(control.addonName(), control.lang('30020'))

        self.endDirectory()

    def addDirectoryItem(self, name, id, action, iconimage, fanart, description):
        url = '{0}?id={1}&action={2}'.format(sysaddon, str(id), str(action))
        item = control.item(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        item.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
        item.setProperty("Fanart_Image", fanart)
        return control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)

    def endDirectory(self, cacheToDisc=True):
        control.directory(int(sys.argv[1]), cacheToDisc=cacheToDisc)
