# -*- coding: utf-8 -*-

"""
    TheDabur Add-on
    Copyright (C) 2017 TheDabur
"""

from json import loads, dumps
import control


class RPC:
    def __init__(self):
        self.id = 0
        self.body = {"jsonrpc": "2.0", "method": "", "params": "", "id": self.id}

    def run(self, method, params={}):
        self.id += 1
        b = dict(self.body, method=method, params=params, id=self.id)
        req = dumps(b)
        response = control.jsonrpc(req)

        response = loads(response)
        try:
            return response['result']['value']
        except:
            return response
