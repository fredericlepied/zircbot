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
import yaml

from txzmq import ZmqEndpoint
from txzmq import ZmqFactory
from txzmq import ZmqSubConnection
from twisted.internet import reactor, protocol
from twisted.python import log
from twisted.words.protocols import irc
from zircbot.plugins import gerrit
from zircbot.plugins import message
from zircbot.plugins import trello
from zircbot.plugins import sensu

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
        channels = []

        if 'trello' in _CONFIG and _CONFIG['trello']:
            channels += trello.get_channels(_CONFIG['trello'])

        if 'sensu' in _CONFIG and _CONFIG['sensu']:
            channels += sensu.get_channels(_CONFIG['sensu'])

        if 'gerrit' in _CONFIG and _CONFIG['gerrit']:
            channels += gerrit.get_channels(_CONFIG['gerrit'])

        for channel in set(channels):
            self.join(channel)
        log.msg('Connected to IRC server %s:%s' % (_CONFIG['host'],
                                                   _CONFIG['port']))

    def privmsg(self, user, channel, msg):
        nick, _, host = user.partition('!')
        log.msg("{} <{}> {}".format(channel, nick, msg))
        # only answer to message involving the robot's nickname or to
        # a private message
        if msg.find(self.nickname) == -1 and channel != self.nickname:
            log.msg("nothing for me")
            return
        msg = shlex.split(msg.strip())
        if (channel != self.nickname and len(msg) > 1 and
           message[0][-1] == ':'):
            msg = msg[1:]
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
        if 'trello' in data and 'trello' in _CONFIG:
            msg, channels = trello.get_information(_CONFIG['trello'],
                                                   data['trello'])
        elif 'sensu' in data and 'sensu' in _CONFIG:
            msg, channels = sensu.get_information(_CONFIG['sensu'],
                                                  data['sensu'])
        elif 'gerrit' in data and 'gerrit' in _CONFIG:
            msg, channels = gerrit.get_information(_CONFIG['gerrit'],
                                                   data['gerrit'])
        elif 'message' in data and 'message' in _CONFIG:
            msg, channels = message.get_information(_CONFIG['message'],
                                                    data['message'])
        else:
            msg = None
        if msg:
            for channel in channels:
                self.send(channel, msg)

    def send(self, channel, msg):
        self.msg(channel, str(msg))
        log.msg("{}: {}".format(channel, msg))


class IrcFactory(protocol.ReconnectingClientFactory):
    protocol = IrcProtocol


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

# zircbot.py ends here
