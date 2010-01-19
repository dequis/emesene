# -*- coding: utf-8 -*-
'''a module that defines a session object'''

#   This file is part of emesene.
#
#    Emesene is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    emesene is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with emesene; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import time
import Queue

from Worker import EVENTS
from Event import Event
from e3.common.Actions import Actions

import e3
import Logger
from ContactManager import ContactManager

class Session(object):
    NAME = 'Base session'
    DESCRIPTION = '''This is a base session implementation,
    other classes inherit from this one'''
    AUTHOR = 'Mariano Guerra'
    WEBSITE = 'www.emesene.org'

    def __init__(self, id_=None, account=None):
        self.id_ = id_

        if self.id_ is None:
            self.id_ = time.time()

        self._account = None
        self.contacts = None
        self.logger = None
        self.extras = {}

        self.events = Queue.Queue()
        self.actions = Actions()

        if account is not None:
            self.account = account

        self.groups = {}

        self.config = e3.common.Config()
        self.config_dir = e3.common.ConfigDir('emesene2')
        # set the base dir of the config to the base dir plus the account
        self.signals = e3.common.Signals(EVENTS, self.events)

    def _set_account(self, account):
        '''set the value of account'''
        self._account = account
        self.contacts = ContactManager(self._account.account)

        self.config_dir.base_dir = os.path.join(
            self.config_dir.base_dir, self._account.account)
        self.create_config()
        self.logger = Logger.LoggerProcess(self.config_dir.join('log'))
        self.logger.start()

    def _get_account(self):
        '''return the value of account'''
        return self._account

    account = property(fset=_set_account, fget=_get_account)

    def add_event(self, id_, *args):
        '''add an event to the events queue'''
        self.events.put(Event(id_, *args))

    def save_config(self):
        '''save the config of the session'''
        self.config.save(self.config_dir.join('config'))

    def load_config(self):
        '''load the config of the session'''
        # load the global configuration
        self.config.load(os.path.join(self.config_dir.default_base_dir,
            'config'))
        # load the account configuration
        self.config.load(self.config_dir.join('config'))

    def create_config(self):
        '''create all the dirs and files for configuration'''
        self.config_dir.create('')

    def new_conversation(self, account, cid):
        '''start a new conversation with account'''
        self.actions.new_conversation(account, sid)

    def close_conversation(self, cid):
        '''close a conversation identified by cid'''
        self.actions.close_conversation(cid)

    def conversation_invite(self, cid, account):
        '''invite a contact to aconversation identified by cid'''
        self.actions.conv_invite(cid, account)

    def quit(self):
        '''close the worker and socket threads'''
        self.actions.quit()

    def login(self, account, password, status, proxy, use_http=False):
        '''start the login process'''
        raise NotImplementedError('Not implemented')

    def logout(self):
        '''close the session'''
        self.actions.logout()

    def set_status(self, status):
        '''change the status of the session'''
        self.actions.change_status(status)

    def add_contact(self, account):
        '''add the contact to our contact list'''
        self.actions.add_contact(account)

    def remove_contact(self, account):
        '''remove the contact from our contact list'''
        self.actions.remove_contact(account)

    def reject_contact(self, account):
        '''reject a contact that added us'''
        self.actions.reject_contact(account)

    def block(self, account):
        '''block the contact'''
        self.actions.block_contact(account)

    def unblock(self, account):
        '''block the contact'''
        self.actions.unblock_contact(account)

    def set_alias(self, account, alias):
        '''set the alias of a contact'''
        self.actions.set_contact_alias(account, alias)

    def add_to_group(self, account, gid):
        '''add a contact to a group'''
        self.actions.add_to_group(account, gid)

    def remove_from_group(self, account, gid):
        '''remove a contact from a group'''
        self.actions.remove_from_group(account, gid)

    def move_to_group(self, account, src_gid, dest_gid):
        '''remove a contact from the group identified by src_gid and add it
        to dest_gid'''
        self.actions.move_to_group(account, src_gid, dest_gid)

    def add_group(self, name):
        '''add a group '''
        self.actions.add_group(name)

    def remove_group(self, gid):
        '''remove the group identified by gid'''
        self.actions.remove_group(gid)

    def rename_group(self, gid, name):
        '''rename the group identified by gid with the new name'''
        self.actions.rename_group(gid, name)

    def set_nick(self, nick):
        '''set the nick of the session'''
        self.actions.set_nick(nick)

    def set_message(self, message):
        '''set the message of the session'''
        self.actions.set_message(message)

    def set_picture(self, picture_name):
        '''set the picture of the session to the picture with picture_name as
        name'''
        self.actions.set_picture(picture_name)

    def set_preferences(self, preferences):
        '''set the preferences of the session to preferences, that is a
        dict containing key:value pairs where the keys are the preference name
        and value is the new value of that preference'''
        self.actions.set_preference(preferences)

    def send_message(self, cid, text, style=None):
        '''send a common message'''
        raise NotImplementedError('Not implemented')

    def request_attention(self, cid):
        '''request the attention of the contact'''
        raise NotImplementedError('Not implemented')
