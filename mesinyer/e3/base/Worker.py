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
        self.add_queue(session.actions, prefix='_handle_action_')

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
    def _handle_action_add_contact(self, account):
        '''handle Action.ACTION_ADD_CONTACT
        '''
        pass

    def _handle_action_add_group(self, name):
        '''handle Action.ACTION_ADD_GROUP
        '''
        pass

    def _handle_action_add_to_group(self, account, gid):
        '''handle Action.ACTION_ADD_TO_GROUP
        '''
        pass

    def _handle_action_block_contact(self, account):
        '''handle Action.ACTION_BLOCK_CONTACT
        '''
        pass

    def _handle_action_unblock_contact(self, account):
        '''handle Action.ACTION_UNBLOCK_CONTACT
        '''
        pass

    def _handle_action_change_status(self, status_):
        '''handle Action.ACTION_CHANGE_STATUS
        '''
        pass

    def _handle_action_login(self, account, password, status_):
        '''handle Action.ACTION_LOGIN
        '''
        pass

    def _handle_action_logout(self):
        '''handle Action.ACTION_LOGOUT
        '''
        pass

    def _handle_action_move_to_group(self, account, src_gid, dest_gid):
        '''handle Action.ACTION_MOVE_TO_GROUP
        '''
        pass

    def _handle_action_remove_contact(self, account):
        '''handle Action.ACTION_REMOVE_CONTACT
        '''
        pass

    def _handle_action_reject_contact(self, account):
        '''handle Action.ACTION_REJECT_CONTACT
        '''
        pass

    def _handle_action_remove_from_group(self, account, gid):
        '''handle Action.ACTION_REMOVE_FROM_GROUP
        '''
        pass

    def _handle_action_remove_group(self, gid):
        '''handle Action.ACTION_REMOVE_GROUP
        '''
        pass

    def _handle_action_rename_group(self, gid, name):
        '''handle Action.ACTION_RENAME_GROUP
        '''
        pass

    def _handle_action_set_contact_alias(self, account, alias):
        '''handle Action.ACTION_SET_CONTACT_ALIAS
        '''
        pass

    def _handle_action_set_message(self, message):
        '''handle Action.ACTION_SET_MESSAGE
        '''
        pass

    def _handle_action_set_nick(self, nick):
        '''handle Action.ACTION_SET_NICK
        '''
        pass

    def _handle_action_set_picture(self, picture_name):
        '''handle Action.ACTION_SET_PICTURE
        '''
        pass

    def _handle_action_set_preferences(self, preferences):
        '''handle Action.ACTION_SET_PREFERENCES
        '''
        pass

    def _handle_action_new_conversation(self, account, cid):
        '''handle Action.ACTION_NEW_CONVERSATION
        '''
        pass

    def _handle_action_close_conversation(self, cid):
        '''handle Action.ACTION_CLOSE_CONVERSATION
        '''
        pass

    def _handle_action_conv_invite(self, cid, account):
        '''handle Action.ACTION_CONV_INVITE
        '''
        pass

    def _handle_action_send_message(self, cid, message):
        '''handle Action.ACTION_SEND_MESSAGE
        cid is the conversation id, message is a MsnMessage object
        '''
        pass

    def _handle_action_send_oim(self, cid, dest, message):
        '''handle Action.ACTION_SEND_OIM
        cid is the conversation id, message is a string
        dest is the oim receiver account
        '''
        pass

    # p2p handlers

    def _handle_action_p2p_invite(self, cid, pid, dest, type_, identifier):
        '''handle Action.ACTION_P2P_INVITE,
         cid is the conversation id
         pid is the p2p session id, both are numbers that identify the
            conversation and the session respectively, time.time() is
            recommended to be used.
         dest is the destination account
         type_ is one of the e3.Transfer.TYPE_* constants
         identifier is the data that is needed to be sent for the invitation
        '''
        pass

    def _handle_action_p2p_accept(self, pid):
        '''handle Action.ACTION_P2P_ACCEPT'''
        pass

    def _handle_action_p2p_cancel(self, pid):
        '''handle Action.ACTION_P2P_CANCEL'''
        pass
