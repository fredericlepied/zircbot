#
# Copyright (C) 2015 Red Hat, Inc.
#
# Author: Frederic Lepied <frederic.lepied@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import sys
import unittest

from twisted.python import log
import zircbot


log.startLogging(sys.stdout)


def validate(obj, json_str, output):
    result = zircbot.plugins.sensu.to_message(json.loads(json_str)['sensu'])
    obj.assertEquals(result, output)


class TestSensuSerialization(unittest.TestCase):

    def test_action_resolve(self):
        validate(self, ACTION_RESOLVE,
                           '(monitoring) RESOLVE: uchiwa - CheckPort OK: All '
                           'ports (80) are accessible for host 0.0.0.0')

    def test_action_create(self):
        validate(self, ACTION_CREATE,
                           '(monitoring) ALERT: uchiwa - CheckPort CRITICAL: '
                           'Connection refused by 0.0.0.0:80')

ACTION_RESOLVE = '{ "sensu" : { "id": "9f4c5e36-e08b-4b04-99a7-2c5806a8177c", "dcid": "mydc", "client": { "name": "monitoring", "address": "127.0.0.1", "subscriptions": [ "base" ], "version": "0.21.0", "timestamp": 1453302198 }, "check": { "command": "check-ports.rb -h 0.0.0.0 -p 80 -t 30", "interval": 10, "standalone": true, "handlers": [ "irc", "file" ], "name": "uchiwa", "issued": 1453302212, "executed": 1453302212, "duration": 0.13, "output": "CheckPort OK: All ports (80) are accessible for host 0.0.0.0", "status": 0, "history": [ "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "0" ], "total_state_change": 6 }, "occurrences": 114, "action": "resolve", "timestamp": 1453302212 }}'

ACTION_CREATE = '{ "sensu" : {"id": "2d344dc8-5f3b-457a-acb9-3674a21d75f7", "dcid": "mydc", "client": { "name": "monitoring", "address": "46.231.133.106", "subscriptions": [ "base" ], "version": "0.21.0", "timestamp": 1453389843 }, "check": { "command": "check-ports.rb -h 0.0.0.0 -p 80 -t 30", "interval": 10, "standalone": true, "handlers": [ "irc", "file" ], "name": "uchiwa", "issued": 1453389848, "executed": 1453389848, "duration": 0.145, "output": "CheckPort CRITICAL: Connection refused by 0.0.0.0:80", "status": 2, "history": [ "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2" ], "total_state_change": 0 }, "occurrences": 22, "action": "create", "timestamp": 1453389849 }}'
