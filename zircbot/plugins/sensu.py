#
# Copyright (C) 2016 Red Hat, Inc.
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

import traceback
from twisted.python import log


def get_channels(data):
    '''Return the list of channels the zircbot should connect to
       notify sensu events'''

    return sum(data.values(), [])


def get_information(ctx, data):
    try:
        message = to_message(data)
        channels = ctx[data['dcid']]

        return message, channels
    except Exception:
        return None, None


def to_message(data):
    try:
        return '(%s) %s: %s - %s' % (get_client_name(data),
                                     get_action(data).upper(),
                                     get_check_name(data),
                                     get_check_output(data).rstrip())
    except:
        log.msg('error decoding data %s:' % data)
        log.msg(traceback.format_exc())
    return None


def get_client_name(data):
    return data['client']['name']


def get_action(data):
    action = data['action']
    if data['action'] == 'create':
        action = 'alert'
    return action


def get_check_name(data):
    return data['check']['name']


def get_check_output(data):
    return data['check']['output']
