zircbot
=======

zircbot is an IRC bot that relays notification from 0mq messages. It
now supports trello notifications (see
https://github.com/fredericlepied/ztrellohook) and sensu
notifications.

Installation
++++++++++++

Using tox, you can provision the needed dependencies using the
following commands::
  
  $ tox -epy27
  $ . .tox/py27/bin/activate

Then copy ``config-sample.yml`` into ``config.yml`` and edit it to
suit your needs.

You can then launch the server using the following command::
  
  $ zircbot
