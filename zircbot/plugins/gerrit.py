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

import re
import sys
import traceback

from twisted.python import log

log.startLogging(sys.stdout)


def get_channels(data):
    '''Return the list of channels the zircbot should connect to
       notify gerrit events'''

    for key in data.keys():
        data[re.compile(key)] = data[key]
        del data[key]
    return sum(data.values(), [])


def get_information(cfg, data):
    message, project = to_message(data)
    channels = []

    if project:
        for regexp in cfg:
            if regexp.search(project):
                channels = cfg[regexp]
                break
    return message, channels


def to_message(data):
    try:
        if data['type'] == 'patchset-created':
            return ('%s proposed to %s: %s: %s' %
                    (data['change']['owner']['name'],
                     data['change']['project'],
                     data['change']['commitMessage'].split('\n')[0],
                     data['change']['url']), data['change']['project'])
        elif data['type'] in ('ref-replicated', 'comment-added',
                              'ref-replication-done', 'change-merged',
                              'reviewer-added', 'ref-updated',
                              'change-restored', 'change-abandoned',
                              'topic-changed'):
            return None, None
        else:
            log.msg('unsupported data %s:' % data)
    except:
        log.msg('error decoding data %s:' % data)
        log.msg(traceback.format_exc())
    return None, None
