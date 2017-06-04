# -*- coding: utf-8 -*-

"""
    TheDabur Add-on
    Copyright (C) 2017 TheDabur
"""

import sys
from time import sleep
import config
import control
import installer
import packages
import rpc as rpc_service
from db import set_enabled


class download:
    def __init__(self):
        pass

    def run(self, action="download", package_id=None):

        conf = config.config()
        rpc = rpc_service.RPC()

        if action == "update":
            try:
                package_id = conf.getPackage()
            except:
                sys.exit(1)

        if package_id is None:
            sys.exit(1)

        packages_instance = packages.packages()
        package_latest_version = packages_instance.getVersion()

        package = packages_instance.get(package_id)  # Package to install / update
        package_addons = set(package['addons'])  # list of addons belong to package
        package_zips = package['zip']

        current_addons = conf.getAddons()  # current addons exists in config.ini
        try:
            installed_addons = set([a['addonid'] for a in rpc.run("Addons.GetAddons")['result']['addons']
                                    if not a['addonid'].startswith('skin.')])
        except:
            raise

        try:
            enabled_addons = sorted(
                [a['addonid'] for a in rpc.run("Addons.GetAddons", {'enabled': True})['result']['addons']])
        except:
            enabled_addons = []

        addons_to_remove = sorted(current_addons - package_addons)
        addons_to_install = sorted(package_addons - installed_addons)

        dp = control.progressDialog
        dp.create(control.addonName())

        inst = installer.Installer(control.addonInfo('id'), dp, control.lang(30005))
        inst.clear_all(sorted(addons_to_remove))

        index = 1
        count = len(package_zips) + len(addons_to_install)
        for package_zip in package_zips:
            package_zip = package_zip.replace('[VER]', package_latest_version)
            inst.download_extract(package_zip, control.transPath('special://home'),
                                  control.lang(30006).format(index, count),
                                  control.lang(30007).format(index, count))
            index += 1

        for addon in addons_to_install:
            inst.get(addon, control.lang(30006).format(index, count), control.lang(30007).format(index, count))
            index += 1

        # Save new config.json
        conf_json = conf.get()
        conf_json['version'] = package_latest_version
        conf_json['package'] = package['id']
        conf_json['addons'] = package['addons']
        conf.save()

        dp.update(0, control.lang(30010))
        control.execute('RefreshRSS')
        dp.update(20)

        # re-enable all addons
        control.execute('UpdateLocalAddons')
        sleep(2)
        addons = sorted(set(inst.packages) | set(enabled_addons))
        set_enabled(addons, True)
        control.execute('UpdateLocalAddons')
        sleep(4)
        dp.close()

        # update skin
        settings = package['settings']
        try:
            skin = settings['lookandfeel.skin']
        except:
            # skin = "skin.eminence.2.mod"
            skin = "skin.estuary"

        rpc.run("Settings.SetSettingValue", {"setting": "locale.language", "value": "english"})
        rpc.run("Settings.SetSettingValue", {"setting": "lookandfeel.font", "value": "Arial"})
        rpc.run("Settings.SetSettingValue", {"setting": "lookandfeel.skin", "value": skin})
        control.execute('Action(Select, 10100)')  # automatically select YES to skin change

        # update settings available in package
        for k, v in settings:
            rpc.run("Settings.SetSettingValue", {"setting": k, "value": v})

        sleep(2)
        control.execute('ReloadSkin')
        control.execute('UpdateAddonRepos')
        control.execute('UpdateLibrary(video)')
        control.execute('ActivateWindow(10000)')
        control.execute('Notification({0},"{1}",5000)'.format(control.addonName(), control.lang(30011).encode('utf-8')))

