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

import json
import sys
import unittest

from twisted.python import log
import zircbot.plugins.gerrit as gerrit


log.startLogging(sys.stdout)


def validate(obj, json_str, output):
    result = gerrit.to_message(json.loads(json_str)['gerrit'])
    obj.assertEquals(result, output)


class TestGerritSerialization(unittest.TestCase):

    def test_move_card(self):
        validate(self, PATCHSET_CREATED_JSON,
                 ('Victor Stinner proposed to openstack/glance: '
                  'Reuse encodeutils.to_utf8(): '
                  'https://review.openstack.org/280713',
                  'openstack/glance'))

PATCHSET_CREATED_JSON = b'''{"gerrit": {"patchSet": {"kind": "REWORK", "author": {"username": "haypo", "name": "Victor Stinner", "email": "vstinner@redhat.com"}, "createdOn": 1456144064, "sizeInsertions": 10, "number": "3", "isDraft": false, "sizeDeletions": -16, "parents": ["89a66916f8fc9a7e1013111f8b2fe44383734690"], "uploader": {"username": "haypo", "name": "Victor Stinner", "email": "vstinner@redhat.com"}, "ref": "refs/changes/13/280713/3", "revision": "ee04a0a0ce34f7a2f664189929924364ce3ba438"}, "type": "patchset-created", "change": {"status": "NEW", "topic": "refactor", "url": "https://review.openstack.org/280713", "commitMessage": "Reuse encodeutils.to_utf8()\\n\\noslo.utils 3.5 got a new to_utf8() function which can be used instead\\nof the common pattern:\\n\\n    if isinstance(text, six.text_type):\\n        text = text.encode(\'utf-8\')\\n\\nUpdate oslo.utils requirements to get at least oslo.utils 3.5.\\n\\nChange-Id: I4c708fa3c6bd18fdd8355fd63b11e43fea3ab6a3\\n", "number": "280713", "project": "openstack/glance", "branch": "master", "owner": {"username": "haypo", "name": "Victor Stinner", "email": "vstinner@redhat.com"}, "id": "I4c708fa3c6bd18fdd8355fd63b11e43fea3ab6a3", "subject": "Reuse encodeutils.to_utf8()"}, "uploader": {"username": "haypo", "name": "Victor Stinner", "email": "vstinner@redhat.com"}, "eventCreatedOn": 1456144064}}'''

if __name__ == "__main__":
    unittest.main()

# test_gerrit_serialization.py ends here
