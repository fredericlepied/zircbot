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
    result = zircbot.plugins.trello.to_message(json.loads(json_str)['trello'])
    obj.assertEquals(result, output)


class TestTrelloSerizalization(unittest.TestCase):

    def test_move_card(self):
        validate(self, CARD_MOVED_JSON,
                 'Frederic Lepied moved to the list "To Do" the card "US5": '
                 'https://trello.com/c/TldNlDYl')

    def test_added(self):
        validate(self, ADDED_JSON,
                 'Frederic Lepied added to the card "US5": '
                 'https://trello.com/c/TldNlDYl')

    def test_removed(self):
        validate(self, REMOVED_JSON,
                 'Frederic Lepied removed from the card "US5":'
                 ' https://trello.com/c/TldNlDYl')

    def test_created(self):
        validate(self, CREATED_CARD,
                 'Frederic Lepied created the card "carte": '
                 'https://trello.com/c/Rwk4EVy0')

    def test_archived(self):
        validate(self, ARCHIVE_JSON,
                 'Frederic Lepied archived the card "carte": '
                 'https://trello.com/c/Rwk4EVy0')

    def test_deleted(self):
        validate(self, DELETE_JSON,
                 'Frederic Lepied deleted the card "45": '
                 'https://trello.com/c/Rwk4EVy0')

    def test_comment(self):
        validate(self, COMMENT_JSON,
                 'Frederic Lepied commented on the card "US44": '
                 'https://trello.com/c/TQbxgAES')

    def test_attachment(self):
        validate(self, ATTACHMENT_JSON,
                 'Frederic Lepied added an attachment to the card "US44": '
                 'http://lwn.net/')

    def test_add_checklist(self):
        validate(self, ADD_CHECKLIST_JSON,
                 'Frederic Lepied added the list "Checklist2" to the card '
                 '"US5": https://trello.com/c/TldNlDYl')

    def test_create_check_item(self):
        validate(self, CREATE_CHECK_ITEM_JSON,
                 'Frederic Lepied added "item1" to the list "Checklist2" of '
                 'the card "US5": https://trello.com/c/TldNlDYl')

    def test_update_check_item(self):
        validate(self, UPDATE_CHECK_ITEM_JSON,
                 'Frederic Lepied checked "pass CI" to the list "Conditions '
                 'of satisfaction" of the card "US5": '
                 'https://trello.com/c/TldNlDYl')

    def test_uncheck_item(self):
        validate(self, UNCHECK_ITEM_JSON,
                 'Frederic Lepied unchecked "pass CI" to the list "Conditions '
                 'of satisfaction" of the card "US5": '
                 'https://trello.com/c/TldNlDYl')

    def test_update_comment(self):
        validate(self, UPDATE_COMMENT_JSON,
                 'Frederic Lepied udpated a comment on the card "US7": '
                 'https://trello.com/c/on2ADFjX')

CARD_MOVED_JSON = '{"trello": {"action": {"type": "updateCard", "idMemberCreator": "5137406a93c18ca34e006232", "memberCreator": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "date": "2015-12-14T18:58:52.564Z", "data": {"listBefore": {"name": "In Progress", "id": "5494215d5d161ca15c8ac4f2"}, "old": {"idList": "5494215d5d161ca15c8ac4f2"}, "board": {"id": "5494190f407d96f733efedca", "name": "Test Board", "shortLink": "I0obloif"}, "card": {"idShort": 25, "id": "5497fb29a42aa12be882402c", "name": "US5", "idList": "5494192403321a4796389930", "shortLink": "TldNlDYl"}, "listAfter": {"name": "To Do", "id": "5494192403321a4796389930"}}, "id": "566f116cbad4979631602343"}, "model": {"descData": null, "labelNames": {"blue": "", "pink": "", "purple": "", "sky": "", "yellow": "", "green": "", "orange": "", "black": "", "red": "", "lime": ""}, "name": "Test Board", "shortUrl": "https://trello.com/b/I0obloif", "idOrganization": null, "pinned": false, "url": "https://trello.com/b/I0obloif/test-board", "closed": false, "prefs": {"permissionLevel": "private", "cardCovers": true, "backgroundColor": "#0079BF", "selfJoin": false, "backgroundBrightness": "unknown", "comments": "members", "invitations": "members", "canBePrivate": true, "canInvite": true, "backgroundImage": null, "backgroundTile": false, "background": "blue", "canBeOrg": true, "cardAging": "regular", "backgroundImageScaled": null, "calendarFeedEnabled": false, "voting": "members", "canBePublic": true}, "id": "5494190f407d96f733efedca", "desc": ""}}}'

ADDED_JSON = '{"trello": {"action": {"type": "addMemberToCard", "member": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "idMemberCreator": "5137406a93c18ca34e006232", "memberCreator": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "date": "2015-12-14T20:31:24.302Z", "data": {"idMember": "5137406a93c18ca34e006232", "board": {"id": "5494190f407d96f733efedca", "name": "Test Board", "shortLink": "I0obloif"}, "card": {"idShort": 25, "id": "5497fb29a42aa12be882402c", "name": "US5", "shortLink": "TldNlDYl"}}, "id": "566f271cb118ab617334f374"}, "model": {"descData": null, "labelNames": {"blue": "", "pink": "", "purple": "", "sky": "", "yellow": "", "green": "", "orange": "", "black": "", "red": "", "lime": ""}, "name": "Test Board", "shortUrl": "https://trello.com/b/I0obloif", "idOrganization": null, "pinned": false, "url": "https://trello.com/b/I0obloif/test-board", "closed": false, "prefs": {"permissionLevel": "private", "cardCovers": true, "backgroundColor": "#0079BF", "selfJoin": false, "backgroundBrightness": "unknown", "comments": "members", "invitations": "members", "canBePrivate": true, "canInvite": true, "backgroundImage": null, "backgroundTile": false, "background": "blue", "canBeOrg": true, "cardAging": "regular", "backgroundImageScaled": null, "calendarFeedEnabled": false, "voting": "members", "canBePublic": true}, "id": "5494190f407d96f733efedca", "desc": ""}}}'

REMOVED_JSON = '{"trello": {"action": {"type": "removeMemberFromCard", "member": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "idMemberCreator": "5137406a93c18ca34e006232", "memberCreator": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "date": "2015-12-14T20:33:29.469Z", "data": {"deactivated": false, "board": {"id": "5494190f407d96f733efedca", "name": "Test Board", "shortLink": "I0obloif"}, "card": {"idShort": 25, "id": "5497fb29a42aa12be882402c", "name": "US5", "shortLink": "TldNlDYl"}, "idMember": "5137406a93c18ca34e006232"}, "id": "566f279959e35e20960ab8e3"}, "model": {"descData": null, "labelNames": {"blue": "", "pink": "", "purple": "", "sky": "", "yellow": "", "green": "", "orange": "", "black": "", "red": "", "lime": ""}, "name": "Test Board", "shortUrl": "https://trello.com/b/I0obloif", "idOrganization": null, "pinned": false, "url": "https://trello.com/b/I0obloif/test-board", "closed": false, "prefs": {"permissionLevel": "private", "cardCovers": true, "backgroundColor": "#0079BF", "selfJoin": false, "backgroundBrightness": "unknown", "comments": "members", "invitations": "members", "canBePrivate": true, "canInvite": true, "backgroundImage": null, "backgroundTile": false, "background": "blue", "canBeOrg": true, "cardAging": "regular", "backgroundImageScaled": null, "calendarFeedEnabled": false, "voting": "members", "canBePublic": true}, "id": "5494190f407d96f733efedca", "desc": ""}}}'

CREATED_CARD = '{"trello": {"action": {"type": "createCard", "idMemberCreator": "5137406a93c18ca34e006232", "memberCreator": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "date": "2015-12-14T20:35:25.651Z", "data": {"list": {"name": "User Stories", "id": "54941921e5193ea1efe744f4"}, "board": {"id": "5494190f407d96f733efedca", "name": "Test Board", "shortLink": "I0obloif"}, "card": {"idShort": 45, "id": "566f280ddcff0bc39616c078", "name": "carte", "shortLink": "Rwk4EVy0"}}, "id": "566f280ddcff0bc39616c079"}, "model": {"descData": null, "labelNames": {"blue": "", "pink": "", "purple": "", "sky": "", "yellow": "", "green": "", "orange": "", "black": "", "red": "", "lime": ""}, "name": "Test Board", "shortUrl": "https://trello.com/b/I0obloif", "idOrganization": null, "pinned": false, "url": "https://trello.com/b/I0obloif/test-board", "closed": false, "prefs": {"permissionLevel": "private", "cardCovers": true, "backgroundColor": "#0079BF", "selfJoin": false, "backgroundBrightness": "unknown", "comments": "members", "invitations": "members", "canBePrivate": true, "canInvite": true, "backgroundImage": null, "backgroundTile": false, "background": "blue", "canBeOrg": true, "cardAging": "regular", "backgroundImageScaled": null, "calendarFeedEnabled": false, "voting": "members", "canBePublic": true}, "id": "5494190f407d96f733efedca", "desc": ""}}}'

ARCHIVE_JSON = '{"trello": {"action": {"type": "updateCard", "idMemberCreator": "5137406a93c18ca34e006232", "memberCreator": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "date": "2015-12-14T20:36:36.679Z", "data": {"old": {"closed": false}, "list": {"name": "User Stories", "id": "54941921e5193ea1efe744f4"}, "board": {"id": "5494190f407d96f733efedca", "name": "Test Board", "shortLink": "I0obloif"}, "card": {"idShort": 45, "id": "566f280ddcff0bc39616c078", "name": "carte", "closed": true, "shortLink": "Rwk4EVy0"}}, "id": "566f28541335ebf3fdac8888"}, "model": {"descData": null, "labelNames": {"blue": "", "pink": "", "purple": "", "sky": "", "yellow": "", "green": "", "orange": "", "black": "", "red": "", "lime": ""}, "name": "Test Board", "shortUrl": "https://trello.com/b/I0obloif", "idOrganization": null, "pinned": false, "url": "https://trello.com/b/I0obloif/test-board", "closed": false, "prefs": {"permissionLevel": "private", "cardCovers": true, "backgroundColor": "#0079BF", "selfJoin": false, "backgroundBrightness": "unknown", "comments": "members", "invitations": "members", "canBePrivate": true, "canInvite": true, "backgroundImage": null, "backgroundTile": false, "background": "blue", "canBeOrg": true, "cardAging": "regular", "backgroundImageScaled": null, "calendarFeedEnabled": false, "voting": "members", "canBePublic": true}, "id": "5494190f407d96f733efedca", "desc": ""}}}'

DELETE_JSON = '{"trello": {"action": {"type": "deleteCard", "idMemberCreator": "5137406a93c18ca34e006232", "memberCreator": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "date": "2015-12-14T20:40:16.650Z", "data": {"list": {"name": "User Stories", "id": "54941921e5193ea1efe744f4"}, "board": {"id": "5494190f407d96f733efedca", "name": "Test Board", "shortLink": "I0obloif"}, "card": {"idShort": 45, "id": "566f280ddcff0bc39616c078", "shortLink": "Rwk4EVy0"}}, "id": "566f2930e9957c76c87c1612"}, "model": {"descData": null, "labelNames": {"blue": "", "pink": "", "purple": "", "sky": "", "yellow": "", "green": "", "orange": "", "black": "", "red": "", "lime": ""}, "name": "Test Board", "shortUrl": "https://trello.com/b/I0obloif", "idOrganization": null, "pinned": false, "url": "https://trello.com/b/I0obloif/test-board", "closed": false, "prefs": {"permissionLevel": "private", "cardCovers": true, "backgroundColor": "#0079BF", "selfJoin": false, "backgroundBrightness": "unknown", "comments": "members", "invitations": "members", "canBePrivate": true, "canInvite": true, "backgroundImage": null, "backgroundTile": false, "background": "blue", "canBeOrg": true, "cardAging": "regular", "backgroundImageScaled": null, "calendarFeedEnabled": false, "voting": "members", "canBePublic": true}, "id": "5494190f407d96f733efedca", "desc": ""}}}'

COMMENT_JSON = '{"trello": {"action": {"type": "commentCard", "idMemberCreator": "5137406a93c18ca34e006232", "memberCreator": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "date": "2015-12-14T20:47:10.236Z", "data": {"text": "comment", "list": {"name": "User Stories", "id": "54941921e5193ea1efe744f4"}, "board": {"id": "5494190f407d96f733efedca", "name": "Test Board", "shortLink": "I0obloif"}, "card": {"idShort": 18, "id": "54975a30b01aaaca5ef22e2a", "name": "US44", "shortLink": "TQbxgAES"}}, "id": "566f2ace4467e9352498485a"}, "model": {"descData": null, "labelNames": {"blue": "", "pink": "", "purple": "", "sky": "", "yellow": "", "green": "", "orange": "", "black": "", "red": "", "lime": ""}, "name": "Test Board", "shortUrl": "https://trello.com/b/I0obloif", "idOrganization": null, "pinned": false, "url": "https://trello.com/b/I0obloif/test-board", "closed": false, "prefs": {"permissionLevel": "private", "cardCovers": true, "backgroundColor": "#0079BF", "selfJoin": false, "backgroundBrightness": "unknown", "comments": "members", "invitations": "members", "canBePrivate": true, "canInvite": true, "backgroundImage": null, "backgroundTile": false, "background": "blue", "canBeOrg": true, "cardAging": "regular", "backgroundImageScaled": null, "calendarFeedEnabled": false, "voting": "members", "canBePublic": true}, "id": "5494190f407d96f733efedca", "desc": ""}}}'

ATTACHMENT_JSON = '{"trello": {"action": {"type": "addAttachmentToCard", "idMemberCreator": "5137406a93c18ca34e006232", "memberCreator": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "date": "2015-12-14T20:49:08.396Z", "data": {"board": {"id": "5494190f407d96f733efedca", "name": "Test Board", "shortLink": "I0obloif"}, "card": {"idShort": 18, "id": "54975a30b01aaaca5ef22e2a", "name": "US44", "shortLink": "TQbxgAES"}, "attachment": {"url": "http://lwn.net/", "name": "http://lwn.net/", "id": "566f2b4453a261e15e860c38"}}, "id": "566f2b4453a261e15e860c39"}, "model": {"descData": null, "labelNames": {"blue": "", "pink": "", "purple": "", "sky": "", "yellow": "", "green": "", "orange": "", "black": "", "red": "", "lime": ""}, "name": "Test Board", "shortUrl": "https://trello.com/b/I0obloif", "idOrganization": null, "pinned": false, "url": "https://trello.com/b/I0obloif/test-board", "closed": false, "prefs": {"permissionLevel": "private", "cardCovers": true, "backgroundColor": "#0079BF", "selfJoin": false, "backgroundBrightness": "unknown", "comments": "members", "invitations": "members", "canBePrivate": true, "canInvite": true, "backgroundImage": null, "backgroundTile": false, "background": "blue", "canBeOrg": true, "cardAging": "regular", "backgroundImageScaled": null, "calendarFeedEnabled": false, "voting": "members", "canBePublic": true}, "id": "5494190f407d96f733efedca", "desc": ""}}}'

ADD_CHECKLIST_JSON = '{"trello": {"action": {"type": "addChecklistToCard", "idMemberCreator": "5137406a93c18ca34e006232", "memberCreator": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "date": "2015-12-16T13:32:58.957Z", "data": {"checklist": {"name": "Checklist2", "id": "5671680ae614058b4dd23d06"}, "board": {"id": "5494190f407d96f733efedca", "name": "Test Board", "shortLink": "I0obloif"}, "card": {"idShort": 25, "id": "5497fb29a42aa12be882402c", "name": "US5", "shortLink": "TldNlDYl"}}, "id": "5671680ae614058b4dd23d07"}, "model": {"descData": null, "labelNames": {"blue": "", "pink": "", "purple": "", "sky": "", "yellow": "", "green": "", "orange": "", "black": "", "red": "", "lime": ""}, "name": "Test Board", "shortUrl": "https://trello.com/b/I0obloif", "idOrganization": null, "pinned": false, "url": "https://trello.com/b/I0obloif/test-board", "closed": false, "prefs": {"permissionLevel": "private", "cardCovers": true, "backgroundColor": "#0079BF", "selfJoin": false, "backgroundBrightness": "unknown", "comments": "members", "invitations": "members", "canBePrivate": true, "canInvite": true, "backgroundImage": null, "backgroundTile": false, "background": "blue", "canBeOrg": true, "cardAging": "regular", "backgroundImageScaled": null, "calendarFeedEnabled": false, "voting": "members", "canBePublic": true}, "id": "5494190f407d96f733efedca", "desc": ""}}}'

CREATE_CHECK_ITEM_JSON = '{"trello": {"action": {"type": "createCheckItem", "idMemberCreator": "5137406a93c18ca34e006232", "memberCreator": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "date": "2015-12-16T14:06:48.002Z", "data": {"checklist": {"name": "Checklist2", "id": "5671680ae614058b4dd23d06"}, "checkItem": {"state": "incomplete", "name": "item1", "id": "56716ff72bb7cf4eb777bc36"}, "board": {"id": "5494190f407d96f733efedca", "name": "Test Board", "shortLink": "I0obloif"}, "card": {"idShort": 25, "id": "5497fb29a42aa12be882402c", "name": "US5", "shortLink": "TldNlDYl"}}, "id": "56716ff82bb7cf4eb777bc37"}, "model": {"descData": null, "labelNames": {"blue": "", "pink": "", "purple": "", "sky": "", "yellow": "", "green": "", "orange": "", "black": "", "red": "", "lime": ""}, "name": "Test Board", "shortUrl": "https://trello.com/b/I0obloif", "idOrganization": null, "pinned": false, "url": "https://trello.com/b/I0obloif/test-board", "closed": false, "prefs": {"permissionLevel": "private", "cardCovers": true, "backgroundColor": "#0079BF", "selfJoin": false, "backgroundBrightness": "unknown", "comments": "members", "invitations": "members", "canBePrivate": true, "canInvite": true, "backgroundImage": null, "backgroundTile": false, "background": "blue", "canBeOrg": true, "cardAging": "regular", "backgroundImageScaled": null, "calendarFeedEnabled": false, "voting": "members", "canBePublic": true}, "id": "5494190f407d96f733efedca", "desc": ""}}}'

UPDATE_CHECK_ITEM_JSON = '{"trello": {"action": {"type": "updateCheckItemStateOnCard", "idMemberCreator": "5137406a93c18ca34e006232", "memberCreator": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "date": "2015-12-16T21:52:48.537Z", "data": {"checklist": {"name": "Conditions of satisfaction", "id": "5497fb37b4c270b1c770ec44"}, "checkItem": {"state": "complete", "name": "pass CI", "id": "5497fb437ea22cb31169da9e"}, "board": {"id": "5494190f407d96f733efedca", "name": "Test Board", "shortLink": "I0obloif"}, "card": {"idShort": 25, "id": "5497fb29a42aa12be882402c", "name": "US5", "shortLink": "TldNlDYl"}}, "id": "5671dd30cdc9b3bc5a471160"}, "model": {"descData": null, "labelNames": {"blue": "", "pink": "", "purple": "", "sky": "", "yellow": "", "green": "", "orange": "", "black": "", "red": "", "lime": ""}, "name": "Test Board", "shortUrl": "https://trello.com/b/I0obloif", "idOrganization": null, "pinned": false, "url": "https://trello.com/b/I0obloif/test-board", "closed": false, "prefs": {"permissionLevel": "private", "cardCovers": true, "backgroundColor": "#0079BF", "selfJoin": false, "backgroundBrightness": "unknown", "comments": "members", "invitations": "members", "canBePrivate": true, "canInvite": true, "backgroundImage": null, "backgroundTile": false, "background": "blue", "canBeOrg": true, "cardAging": "regular", "backgroundImageScaled": null, "calendarFeedEnabled": false, "voting": "members", "canBePublic": true}, "id": "5494190f407d96f733efedca", "desc": ""}}}'

UNCHECK_ITEM_JSON = '{"trello": {"action": {"type": "updateCheckItemStateOnCard", "idMemberCreator": "5137406a93c18ca34e006232", "memberCreator": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "date": "2015-12-16T21:59:01.579Z", "data": {"checklist": {"name": "Conditions of satisfaction", "id": "5497fb37b4c270b1c770ec44"}, "checkItem": {"state": "incomplete", "name": "pass CI", "id": "5497fb437ea22cb31169da9e"}, "board": {"id": "5494190f407d96f733efedca", "name": "Test Board", "shortLink": "I0obloif"}, "card": {"idShort": 25, "id": "5497fb29a42aa12be882402c", "name": "US5", "shortLink": "TldNlDYl"}}, "id": "5671dea5432715ced9e7b8a1"}, "model": {"descData": null, "labelNames": {"blue": "", "pink": "", "purple": "", "sky": "", "yellow": "", "green": "", "orange": "", "black": "", "red": "", "lime": ""}, "name": "Test Board", "shortUrl": "https://trello.com/b/I0obloif", "idOrganization": null, "pinned": false, "url": "https://trello.com/b/I0obloif/test-board", "closed": false, "prefs": {"permissionLevel": "private", "cardCovers": true, "backgroundColor": "#0079BF", "selfJoin": false, "backgroundBrightness": "unknown", "comments": "members", "invitations": "members", "canBePrivate": true, "canInvite": true, "backgroundImage": null, "backgroundTile": false, "background": "blue", "canBeOrg": true, "cardAging": "regular", "backgroundImageScaled": null, "calendarFeedEnabled": false, "voting": "members", "canBePublic": true}, "id": "5494190f407d96f733efedca", "desc": ""}}}'

UPDATE_COMMENT_JSON = '{"trello": {"action": {"type": "updateComment", "idMemberCreator": "5137406a93c18ca34e006232", "memberCreator": {"username": "fredericlepied", "fullName": "Frederic Lepied", "initials": "FL", "id": "5137406a93c18ca34e006232", "avatarHash": "3844765cb385eb13674402d3f33aadc4"}, "date": "2016-01-04T16:47:55.228Z", "data": {"action": {"text": "comment 3", "id": "568a9b6039874dd560717f81"}, "old": {"text": "comment2"}, "board": {"id": "5494190f407d96f733efedca", "name": "Test Board", "shortLink": "I0obloif"}, "card": {"idShort": 26, "id": "5499608d2127f1851b636350", "name": "US7", "shortLink": "on2ADFjX"}}, "id": "568aa23b550965e359051b1d"}, "model": {"descData": null, "labelNames": {"blue": "", "pink": "", "purple": "", "sky": "", "yellow": "", "green": "", "orange": "", "black": "", "red": "", "lime": ""}, "name": "Test Board", "shortUrl": "https://trello.com/b/I0obloif", "idOrganization": null, "pinned": false, "url": "https://trello.com/b/I0obloif/test-board", "closed": false, "prefs": {"permissionLevel": "private", "cardCovers": true, "backgroundColor": "#0079BF", "selfJoin": false, "backgroundBrightness": "unknown", "comments": "members", "invitations": "members", "canBePrivate": true, "canInvite": true, "backgroundImage": null, "backgroundTile": false, "background": "blue", "canBeOrg": true, "cardAging": "regular", "backgroundImageScaled": null, "calendarFeedEnabled": false, "voting": "members", "canBePublic": true}, "id": "5494190f407d96f733efedca", "desc": ""}}}'

if __name__ == "__main__":
    unittest.main()

# test_zircbot.py ends here
