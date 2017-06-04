# -*- coding: utf-8 -*-

"""
    TheDabur Add-on
    Copyright (C) 2017 TheDabur
"""

import xbmc
from xbmc import log as xbmclog
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs

integer = 1

lang = xbmcaddon.Addon().getLocalizedString

addon = xbmcaddon.Addon

addItem = xbmcplugin.addDirectoryItem

item = xbmcgui.ListItem

directory = xbmcplugin.endOfDirectory

content = xbmcplugin.setContent

property = xbmcplugin.setProperty

addonInfo = xbmcaddon.Addon().getAddonInfo

infoLabel = xbmc.getInfoLabel

jsonrpc = xbmc.executeJSONRPC

window = xbmcgui.Window(10000)

dialog = xbmcgui.Dialog()

progressDialog = xbmcgui.DialogProgress()

windowDialog = xbmcgui.WindowDialog()

button = xbmcgui.ControlButton

image = xbmcgui.ControlImage

keyboard = xbmc.Keyboard

sleep = xbmc.sleep

execute = xbmc.executebuiltin

skin = xbmc.getSkinDir()

openFile = xbmcvfs.File

makeFile = xbmcvfs.mkdir

deleteFile = xbmcvfs.delete

listDir = xbmcvfs.listdir

transPath = xbmc.translatePath

skinPath = xbmc.translatePath('special://skin/')

addonPath = xbmc.translatePath(addonInfo('path'))

dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')


def infoDialog(message, heading=addonInfo('name'), icon='', time=3000):
    try:
        dialog.notification(heading, message, icon, time, sound=False)
    except:
        execute("Notification(%s,%s, %s, %s)" % (heading, message, time, icon))


def yesnoDialog(line1, line2, line3, heading=addonInfo('name'), nolabel='', yeslabel=''):
    return dialog.yesno(heading, line1, line2, line3, nolabel, yeslabel)


def selectDialog(list, heading=addonInfo('name')):
    return dialog.select(heading, list)


def addonName():
    try:
        addon_name = addon().getAddonInfo('name')
    except:
        addon_name = ''

    return addon_name


def version():
    num = ''
    try:
        version = addon().getAddonInfo('version')
    except:
        version = '999'
    for i in version:
        if i.isdigit():
            num += i
        else:
            break
    return int(num)


def refresh():
    return execute('Container.Refresh')


def idle():
    return execute('Dialog.Close(busydialog)')


def log(str, level=xbmc.LOGDEBUG, name=addonName()):
    """
        xbmc.LOGDEBUG   = 0
        xbmc.LOGINFO	= 1
        xbmc.LOGNOTICE  = 2
        xbmc.LOGWARNING = 3
        xbmc.LOGERROR   = 4
        xbmc.LOGSEVERE  = 5
        xbmc.LOGFATAL   = 6
        xbmc.LOGNONE	= 7
    """
    xbmclog('********** {0}: {1}'.format(name, str), level)
