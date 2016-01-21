#!/usr/bin/env python
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


_CARD_ASSOC = {
    'addMemberToCard': 'added to',
    'removeMemberFromCard': 'removed from',
    'createCard': 'created',
    'deleteCard': 'deleted',
    'commentCard': 'commented on',
    'updateCard': 'updated',
    'addAttachmentToCard': 'added an attachment to',
    'addChecklistToCard': 'not used',
    'createCheckItem': 'not used',
    'updateCheckItemStateOnCard': 'not used',
    'updateComment': 'udpated a comment on',
}


def get_channels(data):
    '''Return the list of channels the zircbot should connect to
       notify trello events'''

    return sum(data.values(), [])


def get_information(ctx, data):
    data = data['trello']

    message = to_message(data)

    board_name = data['action']['data']['board']['shortLink']
    channels = ctx[board_name]

    return message, channels


def to_message(data):
    board_assoc = {
        'addMemberToBoard': 'added to',
        'removeMemberFromBoard': 'removed from',
    }
    try:
        if data['action']['type'] in _CARD_ASSOC:
            if 'member' in data['action']:
                member = 'member'
            else:
                member = 'memberCreator'
            return '%s %s the card "%s": %s' % \
                (data['action'][member]['fullName'],
                 get_action(data['action']),
                 get_card_name(data['action']['data']['card']),
                 get_url(data['action']['data']))
        elif data['action']['type'] in board_assoc:
            return '%s %s the board: %s' % \
                (data['action']['member']['fullName'],
                 board_assoc[data['action']['type']],
                 data['model']['shortUrl'])
        else:
            log.msg('unsupported data %s:' % data)
    except:
        log.msg('error decoding data %s:' % data)
        log.msg(traceback.format_exc())
    return None


def get_card_name(card_data):
    try:
        return card_data['name']
    except KeyError:
        return card_data['idShort']


def get_url(data):
    if 'attachment' in data and 'url' in data['attachment']:
        return data['attachment']['url']
    else:
        return 'https://trello.com/c/' + data['card']['shortLink']


def get_action(data):
    if data['type'] == 'updateCard':
        if 'listAfter' in data['data']:
            return('moved to the list "%s"' %
                   data['data']['listAfter']['name'])
        if 'closed' in data['data']['card'] and \
           data['data']['card']['closed'] is True:
            return('archived')
    elif data['type'] == 'addChecklistToCard':
        return('added the list "%s" to' % data['data']['checklist']['name'])
    elif data['type'] == 'createCheckItem':
        return('added "%s" to the list "%s" of' %
               (data['data']['checkItem']['name'],
                data['data']['checklist']['name']))
    elif data['type'] == 'updateCheckItemStateOnCard':
        return('%schecked "%s" to the list "%s" of' %
               ('' if data['data']['checkItem']['state'] == 'complete'
                else 'un',
                data['data']['checkItem']['name'],
                data['data']['checklist']['name']))
    return _CARD_ASSOC[data['type']]
