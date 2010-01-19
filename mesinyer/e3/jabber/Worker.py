import sys
import time
import xmpp
import Queue

import e3

import logging
log = logging.getLogger('jabber.Worker')

class Worker(e3.Worker):
    '''wrapper of xmpppy to make it work like e3.Worker'''

    NOTIFICATION_DELAY = 60

    def __init__(self, app_name, session, proxy, use_http=False):
        '''class constructor'''
        e3.Worker.__init__(self, app_name, session)
        self.jid = xmpp.protocol.JID(session.account.account)
        self.client = xmpp.Client(self.jid.getDomain(), debug=[])
        #self.client = xmpp.Client(self.jid.getDomain(), debug=['always'])

        self.proxy = proxy
        self.proxy_data = None

        if self.proxy.use_proxy:
            self.proxy_data = {}
            self.proxy_data['host'] = self.proxy.host
            self.proxy_data['port'] = self.proxy.port

            if self.proxy.use_auth:
                self.proxy_data['username'] = self.proxy.user
                self.proxy_data['password'] = self.proxy.passwd

        self.conversations = {}
        self.rconversations = {}
        self.roster = None
        self.start_time = None

    def run_cycle(self):
        if hasattr(self.client, 'Process'):
            self.client.Process(1)

    def run(self):
        e3.Worker.run(self)

        self.session.logger.quit()

    def _on_presence(self, client, presence):
        '''handle the reception of a presence message'''
        message = presence.getStatus() or ''
        show = presence.getShow()
        type_ = presence.getType()
        account = presence.getFrom().getStripped()

        if type_ == 'unavailable':
            stat = e3.status.OFFLINE
        elif show == 'away':
            stat = e3.status.AWAY
        elif show == 'dnd':
            stat = e3.status.BUSY
        else:
            stat = e3.status.ONLINE

        contact = self.session.contacts.contacts.get(account, None)

        if not contact:
            contact = e3.Contact(account)
            self.session.contacts.contacts[account] = contact

        old_message = contact.message
        old_status = contact.status
        contact.message = message
        contact.status = stat

        log_account =  e3.Logger.Account(contact.attrs.get('CID', None), None,
            contact.account, contact.status, contact.nick, contact.message,
            contact.picture)

        if old_status != stat:
            change_type = 'status'

            if old_status == e3.status.OFFLINE:
                change_type = 'online'

            if stat == e3.status.OFFLINE:
                change_type = 'offline'

            do_notify = (self.start_time + Worker.NOTIFICATION_DELAY) < \
                    time.time()

            self.session.add_event(e3.Event.EVENT_CONTACT_ATTR_CHANGED, account,
                change_type, old_status, do_notify)
            self.session.logger.log('status change', stat, str(stat),
                log_account)

        if old_message != contact.message:
            self.session.add_event(e3.Event.EVENT_CONTACT_ATTR_CHANGED, account,
                'message', old_message)
            self.session.logger.log('message change', contact.status,
                contact.message, log_account)

    def _on_message(self, client, message):
        '''handle the reception of a message'''
        body = message.getBody()
        account = message.getFrom().getStripped()

        if account in self.conversations:
            cid = self.conversations[account]
        else:
            cid = time.time()
            self.conversations[account] = cid
            self.rconversations[cid] = [account]
            self.session.add_event(e3.Event.EVENT_CONV_FIRST_ACTION, cid,
                [account])

        if body is None:
            type_ = e3.Message.TYPE_TYPING
        else:
            type_ = e3.Message.TYPE_MESSAGE

        msgobj = e3.Message(type_, body, account)
        self.session.add_event(e3.Event.EVENT_CONV_MESSAGE, cid, account, msgobj)

    # action handlers
    def login(self, account, password, status_):
        if self.client.connect(('talk.google.com', 5223),
                proxy=self.proxy_data) == "":
            self.session.add_event(e3.Event.EVENT_LOGIN_FAILED,
                'Connection error')
            return

        if self.client.auth(self.jid.getNode(),
            self.session.account.password) == None:
            self.session.add_event(e3.Event.EVENT_LOGIN_FAILED,
                'Authentication error')
            return

        self.session.add_event(e3.Event.EVENT_LOGIN_SUCCEED)
        self.start_time = time.time()

        self.client.RegisterHandler('message', self._on_message)

        self.client.sendInitPresence()

        while self.client.Process(1) != '0':
            pass

        self.roster = self.client.getRoster()

        for account in self.roster.getItems():
            name = self.roster.getName(account)

            if account == self.session.account.account:
                if name is not None:
                    self.session.contacts.me.nick = name
                    self.session.add_event(e3.Event.EVENT_NICK_CHANGE_SUCCEED,
                        nick)

                continue

            if account in self.session.contacts.contacts:
                contact = self.session.contacts.contacts[account]
            else:
                contact = e3.Contact(account)
                self.session.contacts.contacts[account] = contact

            if name is not None:
                contact.nick = name

        self.session.add_event(e3.Event.EVENT_CONTACT_LIST_READY)
        self.client.RegisterHandler('presence', self._on_presence)

    def logout(self):
        self.client.disconnect()

    def new_conversation(self, account, cid):
        self.conversations[account] = cid
        self.rconversations[cid] = [account]

    def send_message(self, cid, message):
        '''cid is the conversation id, message is a Message object'''

        recipients = self.rconversations.get(cid, ())

        for recipient in recipients:
            self.client.send(xmpp.protocol.Message(recipient, message.body,
                'chat'))
