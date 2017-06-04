# -*- coding: utf-8 -*-

"""
    TheDabur Add-on
    Copyright (C) 2017 TheDabur
"""

import sys
import urlparse

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))

try:
    action = params['action']
except:
    action = None
try:
    package_id = params['id']
except:
    package_id = None

if action is None:
    from resources.lib import menu

    menu.menu().root()

elif action == 'download' or action == "update":
    from resources.lib import download

    download.download().run(action, package_id)

elif action == 'restore':
    pass
