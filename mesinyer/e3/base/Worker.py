'''a thread that handles the connection with the main server'''

import Queue
import threading

from Event import Event
from Thread import Thread

import e3

EVENTS = (\
 'login started'         , 'login info'           ,
 'login succeed'         , 'login failed'         ,
 'disconnected'          , 'contact list ready'   ,
 'contact attr changed'  , 'contact added'        ,
 'contact add succeed'   , 'contact add failed'   ,
 'contact remove succeed', 'contact remove failed',
 'contact reject succeed', 'contact reject failed',
 'contact move succeed'  , 'contact move failed'  ,
 'contact copy succeed'  , 'contact copy failed'  ,
 'contact block succeed' , 'contact block failed' ,
 'contact unblock succeed' , 'contact unblock failed',
 'contact alias succeed' , 'contact alias failed' ,
 'group add succeed'     , 'group add failed'     ,
 'group remove succeed'  , 'group remove failed'  ,
 'group rename succeed'  , 'group rename failed'  ,
 'group add contact succeed'     , 'group add contact failed'   ,
 'group remove contact succeed'  , 'group remove contact failed',
 'status change succeed' , 'status change failed' ,
 'nick change succeed'   , 'nick change failed'   ,
 'message change succeed', 'message change failed',
 'picture change succeed', 'error'                ,
 'conv contact joined'   , 'conv contact left'  ,
 'conv started'          , 'conv ended'           ,
 'conv group started'    , 'conv group ended'     ,
 'conv message'          , 'conv first action'    ,
 'conv message send succeed'  , 'conv message send failed',
 'oim received',       'oims data received',
 'p2p invitation',      'p2p finished',
 'p2p error',           'p2p canceled',
 'p2p accepted',        'p2p progress',
 'profile get succeed'  , 'profile get failed',
 'profile set succeed'  , 'profile set failed',
 'media received')

Event.set_constants(EVENTS)

actions = []
def action(f):
    actions.append(f.__name__)
    return f

class Worker(Thread):
    '''this class represent an object that waits for commands from the queue
    of a socket, process them and add it as events to its own queue'''

    def __init__(self, app_name, session):
        '''class constructor'''
        Thread.__init__(self)
        self.setDaemon(True)

        self.app_name = app_name

        self.in_login = False
        self.session = session
        self.add_queue(session.actions)

        # this queue receives a Command object
        self.command_queue = Queue.Queue()

        self.action_handlers = {}

    def run_cycle(self):
        '''main method, block waiting for data, process it, and send data back
        '''
        raise NotImplentedError('not implemented')

    def _process_action(self, action):
        '''process an action'''
        if action.id_ in self.action_handlers:
            try:
                self.action_handlers[action.id_](*action.args)
            except TypeError:
                self.session.add_event(Event.EVENT_ERROR,
                    'Error calling action handler', action.id_)


    # action handlers (the stubs, copy and complete them on your implementation)
    @action
    def add_contact(self, account):
        pass

    @action
    def add_group(self, name):
        pass

    @action
    def add_to_group(self, account, gid):
        pass

    @action
    def block_contact(self, account):
        pass

    @action
    def unblock_contact(self, account):
        pass

    @action
    def change_status(self, status_):
        pass

    @action
    def login(self, account, password, status_):
        pass

    @action
    def logout(self):
        pass

    @action
    def move_to_group(self, account, src_gid, dest_gid):
        pass

    @action
    def remove_contact(self, account):
        pass

    @action
    def reject_contact(self, account):
        pass

    @action
    def remove_from_group(self, account, gid):
        pass

    @action
    def remove_group(self, gid):
        pass

    @action
    def rename_group(self, gid, name):
        pass

    @action
    def set_contact_alias(self, account, alias):
        pass

    @action
    def set_message(self, message):
        pass

    @action
    def set_nick(self, nick):
        pass

    @action
    def set_picture(self, picture_name):
        pass

    @action
    def set_preferences(self, preferences):
        pass

    @action
    def new_conversation(self, account, cid):
        pass

    @action
    def close_conversation(self, cid):
        pass

    @action
    def conv_invite(self, cid, account):
        pass

    @action
    def send_message(self, cid, message):
        '''cid is the conversation id, message is a MsnMessage object'''
        pass

    @action
    def send_oim(self, cid, dest, message):
        '''cid is the conversation id, message is a string
        dest is the oim receiver account
        '''
        pass

    # p2p handlers

    @action
    def p2p_invite(self, cid, pid, dest, type_, identifier):
        '''cid is the conversation id
        pid is the p2p session id, both are numbers that identify the
         conversation and the session respectively, time.time() is
         recommended to be used.
        dest is the destination account
        type_ is one of the e3.Transfer.TYPE_* constants
        identifier is the data that is needed to be sent for the invitation
        '''
        pass

    @action
    def p2p_accept(self, pid):
        pass

    @action
    def p2p_cancel(self, pid):
        pass
