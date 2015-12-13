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

'''
IRC bot that forward 0mq messages to IRC chans.

It subscribes to a pub server and forward the message to the
configured IRC chans.
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


def say(msg, channel, message):
    msg(channel, str(message))
    log.msg("{}: {}".format(channel, message))


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
        for channel in _CONFIG["channels"]:
            self.join(channel)
        log.msg('Connected to IRC server %s:%s' % (_CONFIG['host'],
                                                   _CONFIG['port']))

    def privmsg(self, user, channel, message):
        nick, _, host = user.partition('!')
        log.msg("{} <{}> {}".format(channel, nick, message))
        message = shlex.split(message.strip())
        if channel != _CONFIG['nickname'] and len(message) > 1:
            message = message[1:]
        if channel == _CONFIG['nickname']:
            channel = nick
            prefix = ''
        else:
            prefix = '%s: ' % nick
        say(self.msg, channel,
            "%sI just forward messages. I don\'t know what '%s' mean ;-)" %
            (prefix, message[0]))

    def forward(self, data):
        if 'trello' in data:
            message = trello_to_message(data['trello'])
        else:
            message = None
        if message:
            for channel in _CONFIG['channels']:
                say(self.msg, channel, message)


class IrcFactory(protocol.ReconnectingClientFactory):
    protocol = IrcProtocol


def trello_to_message(data):
    try:
        if data['action']['type'] == 'addMemberToCard':
            return '%s added to the card "%s": %s/%s' % \
                (data['action']['member']['fullName'],
                 data['action']['data']['card']['name'],
                 'https://trello.com/c',
                 data['action']['data']['card']['shortLink'])
        elif data['action']['type'] == 'removeMemberFromCard':
            return '%s removed from the card "%s": %s/%s' % \
                (data['action']['member']['fullName'],
                 data['action']['data']['card']['name'],
                 'https://trello.com/c',
                 data['action']['data']['card']['shortLink'])
        elif data['action']['type'] == 'createCard':
            return '%s created the card "%s": %s/%s' % \
                (data['action']['memberCreator']['fullName'],
                 data['action']['data']['card']['name'],
                 'https://trello.com/c',
                 data['action']['data']['card']['shortLink'])
        elif data['action']['type'] == 'commentCard':
            return '%s commented on the card "%s": %s/%s' % \
                (data['action']['memberCreator']['fullName'],
                 data['action']['data']['card']['name'],
                 'https://trello.com/c',
                 data['action']['data']['card']['shortLink'])
        elif data['action']['type'] == 'updateCard':
            return '%s updated the card "%s": %s/%s' % \
                (data['action']['memberCreator']['fullName'],
                 data['action']['data']['card']['name'],
                 'https://trello.com/c',
                 data['action']['data']['card']['shortLink'])
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

main()

# zircbot.py ends here
