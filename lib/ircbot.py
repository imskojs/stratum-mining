import base64
import gc
import json
import os
import random
import sys
import time
import signal
import traceback
import urlparse
import twisted
import settings
#if settings.BOT_ENABLED:
from twisted.words.protocols import irc
class IRCClient(irc.IRCClient):
   nickname = settings.BOT_NICK
   channel = settings.BOT_CHANNEL
   
   def lineReceived(self, line):
       log.debug(line)
       irc.IRCClient.lineReceived(self, line)
   
   def signedOn(self):
       self.in_channel = False
       irc.IRCClient.signedOn(self)
       self.factory.resetDelay()
       self.join(self.channel)
   
   @defer.inlineCallbacks
   def new_share(share):
       if not self.in_channel:
          return
       if share.pow_hash <= share.header['bits'].target and abs(share.timestamp - time.time()) < 10*60:
          yield deferral.sleep(random.expovariate(1/60))
          message = '\x02%s BLOCK FOUND by %s! %s%064x' % (net.NAME.upper(), bitcoin_data.script2_to_address(share.new_script, net.PARENT), net.PARENT.BLOCK_EXPLORER_URL_PREFIX, share.header_hash)
          if all('%x' % (share.header_hash,) not in old_message for old_message in self.recent_messages):
          self.say(self.channel, message)
          self._remember_message(message)
          self.watch_id = node.tracker.verified.added.watch(new_share)
          self.recent_messages = []
   
   def joined(self, channel):
       self.in_channel = True
   
   def left(self, channel):
       self.in_channel = False

   def _remember_message(self, message):
      self.recent_messages.append(message)
      while len(self.recent_messages) > 100:
            self.recent_messages.pop(0)
 
   def privmsg(self, user, channel, message):
       if channel == self.channel:
          self._remember_message(message)
   
   def connectionLost(self, reason):
       node.tracker.verified.added.unwatch(self.watch_id)
       print 'IRC connection lost:', reason.getErrorMessage()

class IRCClientFactory(protocol.ReconnectingClientFactory):
      protocol = IRCClient
      reactor.connectTCP(settings.BOT_NETWORK,settings.BOT_PORT, IRCClientFactory())
