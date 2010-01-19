# -*- coding: utf-8 -*-
import sys
import time
import Queue
import random

import e3

import logging
log = logging.getLogger('dummy.Worker')

class Worker(e3.Worker):
    '''dummy Worker implementation to make it easy to test emesene'''

    def __init__(self, app_name, session, proxy, use_http=False):
        '''class constructor'''
        e3.Worker.__init__(self, app_name, session)
        self.session = session

    def run(self):
        '''main method, block waiting for data, process it, and send data back
        '''
        data = None

        while True:
            try:
                action = self.session.actions.get(True, 0.1)

                if action.id_ == e3.Action.ACTION_QUIT:
                    log.debug('closing thread')
                    self.session.logger.quit()
                    break

                self._process_action(action)
            except Queue.Empty:
                pass

    def _fill_contact_list(self):
        """
        method to fill the contact list with something
        """
        self._add_contact('dx@emesene.org', 'XD', e3.status.ONLINE, '', False)
        self._add_contact('roger@emesene.org', 'r0x0r', e3.status.ONLINE,
                '', False)
        self._add_contact('boyska@emesene.org', 'boyska', e3.status.ONLINE,
                '', True)
        self._add_contact('pochu@emesene.org', '<3 debian', e3.status.BUSY,
                '', False)
        self._add_contact('cloud@emesene.org', 'nube', e3.status.BUSY,
                '', False)
        self._add_contact('otacon@emesene.org', 'Otacon', e3.status.BUSY,
                '', True)
        self._add_contact('federico@emesene.org', 'federico..', e3.status.AWAY,
                'he loves guiness', False)
        self._add_contact('respawner@emesene.org', 'Respawner', e3.status.AWAY,
                '', False)
        self._add_contact('mohrtutchy@emesene.org', 'moh..', e3.status.AWAY,
                'one love', True)
        self._add_contact('nassty@emesene.org', 'nassto', e3.status.IDLE,
                '', False)
        self._add_contact('j0hn@emesene.org', 'juan', e3.status.IDLE, '', False)
        self._add_contact('c0n0@emesene.org', 'conoconocono', e3.status.IDLE,
                '', True)
        self._add_contact('warlo@emesene.org', 'warlo', e3.status.OFFLINE,
                '', False)
        self._add_contact('wariano@emesene.org', 'wariano', e3.status.OFFLINE,
                '', False)
        self._add_contact('Faith_Nahn@emesene.org', 'Gtk styler', e3.status.BUSY,
                '', False)
        self._add_contact('you@emesene.org', 'I\'m on emesene code!',
                e3.status.OFFLINE, '', True)

        self._add_contact('one@hotmail.com', '- [b][c=48]Pαrκ¡[/c=30][/b]', e3.status.BUSY,
                '', False)
        self._add_contact('two@hotmail.com', '[c=46]-๑๑test_test๑๑-[/c=2]', e3.status.BUSY,
                '', False)
        self._add_contact('three@hotmail.com', '[c=29]•°o.Orandom εïз stuff O.o°•[/c=36]·$28', e3.status.BUSY,
                '', False)
        self._add_contact('four@hotmail.com', '[c=48][b]hy[/b][/c=11] ·#·$3,3\'_·$#fcfcfc,#fcfcfc\'_·$4,4\'_·0·$28', e3.status.BUSY,
                '', False)
        self._add_contact('five@hotmail.com', '·&·#·$9X.|̲̅·$10X·$9̲̅·$10x·$9̲̅·$10x·$9̲̅·$10x·$9̲̅·$10x·$9̲̅|·$10·#', e3.status.BUSY,
                '', False)
        self._add_contact('six@hotmail.com', '[c=46][u][b]xafd! [/b][/u][/c]', e3.status.BUSY,
                '', False)
        self._add_contact('seven@hotmail.com', '[c=5]((_...sdsdf..._))..)_<(_))(°.°)(...][/c=48][u][/u]', e3.status.BUSY,
                '', False)

        self._add_group('ninjas')
        self._add_group('pirates')
        self._add_group('lulz')
        self._add_group('code quiz ninjas')
        self._add_group('empty')
        self._add_group('strange nicks')

        self._add_contact_to_group('you@emesene.org', 'pirates')
        self._add_contact_to_group('boyska@emesene.org', 'pirates')
        self._add_contact_to_group('j0hn@emesene.org', 'pirates')
        self._add_contact_to_group('c0n0@emesene.org', 'pirates')
        self._add_contact_to_group('nassty@emesene.org', 'lulz')
        self._add_contact_to_group('warlo@emesene.org', 'lulz')
        self._add_contact_to_group('you@emesene.org', 'lulz')
        self._add_contact_to_group('cloud@emesene.org', 'lulz')
        self._add_contact_to_group('dx@emesene.org', 'ninjas')
        self._add_contact_to_group('roger@emesene.org', 'ninjas')
        self._add_contact_to_group('c0n0@emesene.org', 'ninjas')
        self._add_contact_to_group('boyska@emesene.org', 'ninjas')
        self._add_contact_to_group('Faith_Nahn@emesene.org', 'code quiz ninjas')

        self._add_contact_to_group('one@hotmail.com', 'strange nicks')
        self._add_contact_to_group('two@hotmail.com', 'strange nicks')
        self._add_contact_to_group('three@hotmail.com', 'strange nicks')
        self._add_contact_to_group('four@hotmail.com', 'strange nicks')
        self._add_contact_to_group('five@hotmail.com', 'strange nicks')
        self._add_contact_to_group('six@hotmail.com', 'strange nicks')
        self._add_contact_to_group('seven@hotmail.com', 'strange nicks')

    def _add_contact(self, mail, nick, status_, alias, blocked):
        """
        method to add a contact to the contact list
        """
        self.session.contacts.contacts[mail] = e3.Contact(mail, mail,
            nick, '...', status_, alias, blocked)

    def _add_group(self, name):
        """
        method to add a group to the contact list
        """
        self.session.groups[name] = e3.Group(name, name)

    def _add_contact_to_group(self, account, group):
        """
        method to add a contact to a group
        """
        self.session.groups[group].contacts.append(account)
        self.session.contacts.contacts[account].groups.append(group)

    # action handlers
    def add_contact(self, account):
        self.session.add_event(e3.Event.EVENT_CONTACT_ADD_SUCCEED,
            account)

    def add_group(self, name):
        self.session.add_event(e3.Event.EVENT_GROUP_ADD_SUCCEED,
            name)

    def add_to_group(self, account, gid):
        self.session.add_event(e3.Event.EVENT_GROUP_ADD_CONTACT_SUCCEED,
            gid, account)

    def block_contact(self, account):
        self.session.add_event(e3.Event.EVENT_CONTACT_BLOCK_SUCCEED, account)

    def unblock_contact(self, account):
        self.session.add_event(e3.Event.EVENT_CONTACT_UNBLOCK_SUCCEED,
            account)

    def change_status(self, status_):
        self.session.account.status = status_
        self.session.contacts.me.status = status_
        self.session.add_event(e3.Event.EVENT_STATUS_CHANGE_SUCCEED, status_)

    def login(self, account, password, status_):
        self.session.add_event(e3.Event.EVENT_LOGIN_SUCCEED)
        self.session.add_event(e3.Event.EVENT_NICK_CHANGE_SUCCEED,
                'dummy nick is dummy')
        self._fill_contact_list()
        self.session.add_event(e3.Event.EVENT_CONTACT_LIST_READY)

    def move_to_group(self, account, src_gid, dest_gid):
        self.session.add_event(e3.Event.EVENT_CONTACT_MOVE_SUCCEED,
            account, src_gid, dest_gid)

    def remove_contact(self, account):
        self.session.add_event(e3.Event.EVENT_CONTACT_REMOVE_SUCCEED, account)

    def reject_contact(self, account):
        self.session.add_event(e3.Event.EVENT_CONTACT_REJECT_SUCCEED, account)

    def remove_from_group(self, account, gid):
        self.session.add_event(e3.Event.EVENT_GROUP_REMOVE_CONTACT_SUCCEED,
            gid, account)

    def remove_group(self, gid):
        self.session.add_event(e3.Event.EVENT_GROUP_REMOVE_SUCCEED, gid)

    def rename_group(self, gid, name):
        self.session.add_event(e3.Event.EVENT_GROUP_RENAME_SUCCEED,
            gid, name)

    def set_contact_alias(self, account, alias):
        self.session.add_event(e3.Event.EVENT_CONTACT_ALIAS_SUCCEED, account)

    def set_message(self, message):
        self.session.add_event(e3.Event.EVENT_MESSAGE_CHANGE_SUCCEED, message)

    def set_nick(self, nick):
        self.session.add_event(e3.Event.EVENT_NICK_CHANGE_SUCCEED, nick)

    def set_picture(self, picture_name):
        self.session.contacts.me.picture = picture_name
        self.session.add_event(e3.Event.EVENT_PICTURE_CHANGE_SUCCEED,
                self.session.account.account, picture_name)

    def send_message(self, cid, message):
        '''cid is the conversation id, message is a Message object'''
        self.session.add_event(e3.Event.EVENT_CONV_MESSAGE_SEND_SUCCEED,
            cid, message)
        account = random.choice(self.session.contacts.contacts.keys())
        self.session.add_event(e3.Event.EVENT_CONV_MESSAGE,
            cid, account, message)
