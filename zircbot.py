#!/usr/bin/env python
#
# Copyright (C) 2015 Red Hat, Inc.
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

'''IRC bot that forward 0mq messages to IRC chans.

It subscribes to a pub server, interpret the JSON data into a message
and then forward the message to the configured IRC chans.

'''

import json
import shlex
import sys
import traceback
import yaml

from txzmq import ZmqEndpoint
from txzmq import ZmqFactory
from txzmq import ZmqSubConnection
from twisted.internet import reactor, protocol
from twisted.python import log
from twisted.words.protocols import irc

_CONFIG = None
_IRC_PROTOCOL = None


class IrcProtocol(irc.IRCClient):
    # TODO: find a clean way to do that
    def __init__(self):
        global _IRC_PROTOCOL
        _IRC_PROTOCOL = self

        self.nickname = _CONFIG['nickname']
        self.password = _CONFIG['password']
        self.username = _CONFIG['nickname']
        self.versionName = "ZircBot v0.0.1"
        self.versionNum = "0.0.1"
        self.realname = _CONFIG['nickname']

    def signedOn(self):
        channels = set()
        for board_name in _CONFIG['trello'].keys():
            for channel in _CONFIG['trello'][board_name]:
                channels.add(channel)
        for channel in channels:
            self.join(channel)
        log.msg('Connected to IRC server %s:%s' % (_CONFIG['host'],
                                                   _CONFIG['port']))

    def privmsg(self, user, channel, message):
        nick, _, host = user.partition('!')
        log.msg("{} <{}> {}".format(channel, nick, message))
        # only answer to message involving the robot's nickname or to
        # a private message
        if message.find(self.nickname) == -1 and channel != self.nickname:
            log.msg("nothing for me")
            return
        message = shlex.split(message.strip())
        if (channel != self.nickname and len(message) > 1 and
           message[0][-1] == ':'):
            message = message[1:]
        if channel == self.nickname:
            channel = nick
            prefix = ''
        else:
            prefix = '%s: ' % nick
        self.send(
            channel,
            "%sI just forward messages. I don\'t know what '%s' mean ;-)" %
            (prefix, message[0]))

    def forward(self, data):
        if 'trello' in data:
            trello_data = data['trello']
            message = trello_to_message(trello_data)
            try:
                bd_name = trello_data['action']['data']['board']['shortLink']
                channels = _CONFIG['trello'][bd_name]
            except KeyError:
                channels = []
        else:
            message = None
        if message:
            for channel in channels:
                self.send(channel, message)

    def send(self, channel, message):
        self.msg(channel, str(message))
        log.msg("{}: {}".format(channel, message))


class IrcFactory(protocol.ReconnectingClientFactory):
    protocol = IrcProtocol


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


_CARD_ASSOC = {
    'addMemberToCard': 'added to',
    'removeMemberFromCard': 'removed from',
    'createCard': 'created',
    'deleteCard': 'deleted',
    'commentCard': 'commented on',
    'updateCard': 'updated',
    'addAttachmentToCard': 'added an attachment to',
}


def get_action(data):
    if data['type'] == 'updateCard':
        if 'listAfter' in data['data']:
            return('moved to the list "%s"' %
                   data['data']['listAfter']['name'])
        if ('closed' in data['data']['card'] and
            data['data']['card']['closed'] == True):
            return('archived')
    return _CARD_ASSOC[data['type']]


def trello_to_message(data):
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
    except Exception:
        log.msg('error decoding data %s:' % data)
        log.msg(traceback.format_exc())
    return None


def main():
    global _CONFIG

    with open('config.yml') as f:
        _CONFIG = yaml.load(f.read())

    log.startLogging(sys.stderr)

    ircf = IrcFactory()
    reactor.connectTCP(_CONFIG['host'], _CONFIG['port'], ircf)

    zf = ZmqFactory()
    e = ZmqEndpoint(_CONFIG['method'], _CONFIG['endpoint'])

    s = ZmqSubConnection(zf, e)
    s.subscribe("")

    def do_forward(*args):
        if _IRC_PROTOCOL:
            _IRC_PROTOCOL.forward(json.loads(args[0]))

    s.gotMessage = do_forward

    reactor.run()

if __name__ == "__main__":
    main()

# zircbot.py ends here
