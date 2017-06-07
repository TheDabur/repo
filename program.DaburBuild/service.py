import sys
from time import sleep, time
from resources.lib import control, packages, config

conf = config.config()
conf_json = conf.get()
current_version = conf.getVersion()
updated_at = conf.getUpdatedAt()
update_next_check = conf.getUpdateNextCheck()

# protect flood Github and make sure we do the check only when update_next_check is less then now
if update_next_check > int(time()):
    sys.exit(1)

packages_instance = packages.packages()
package_latest_version = packages_instance.getVersion()

conf_json['update_next_check'] = int(time()) + config.CONFIG_NEXT_UPDATE_INTERVAL
conf.save()

# if the current version is the same as the latest we don't need to prompt update
if current_version == package_latest_version:
    sys.exit(1)

# if skip_version is exists and its the same as the latest package version
# its mean he user chose to skip this update
if "skip_version" in conf_json and conf_json['skip_version'] == package_latest_version:
    sys.exit(1)

# Lets wait a bit before prompt
sleep(20)
if control.yesnoDialog(control.lang(30040).format(package_latest_version), "", "", control.addonInfo('name'),
                       control.lang(30032), control.lang(30031)):

    if "skip_version" in conf_json:
        del conf_json['skip_version']

    conf_json['updated_at'] = int(time())
    conf.save()
    control.execute('RunScript({0}, 0, action=update)'.format(control.addonInfo('id')))
else:
    if control.yesnoDialog(control.lang(30042), "", "", control.addonInfo('name'), control.lang(30032), control.lang(30031)):
        conf_json['update_next_check'] = int(time()) + config.CONFIG_NEXT_UPDATE_INTERVAL + 60*60*24*3

        if "skip_version" in conf_json:
            del conf_json['skip_version']

        conf.save()
    else:
        conf_json['skip_version'] = package_latest_version
        conf.save()

