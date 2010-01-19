import Queue
import logging
import threading

from e3.common.Actions import Actions

log = logging.getLogger('e3.Thread')

class Thread(threading.Thread):
    '''A thread that reads actions from queues and calls the corresponding
    methods'''

    def __init__(self):
        threading.Thread.__init__(self)
        self._queues = []

    def add_queue(self, queue=None, object=None, prefix=''):
        '''Adds an Actions queue to the list
        object and prefix are used to get the method name like this:
            (object).(prefix)(action)
        With default values and an action called "action" it would be:
            self.action()
        '''
        queue = queue or Actions()
        object = object or self
        self._queues.append((queue, object, prefix))

    def run_cycle(self):
        pass

    def run(self):
        '''The thread main loop
        Override this and call Thread.run(self) to put code before or after
        '''
        log.info("Starting thread %s", repr(self))
        while True:
            try:
                if self.run_cycle() == False:
                    continue

                for queue, object, prefix in self._queues:
                    try:
                        action, args, kwds = queue.get(True, 0.1)
                    except Queue.Empty:
                        continue
                    
                    if hasattr(object, prefix + action):
                        getattr(object, prefix + action)(*args, **kwds)
                    elif action == 'quit':
                        break
                    else:
                        log.warning("No such function %s.%s%s", object, prefix, action)
            except Quit:
                break
        log.info("Closing thread %s", repr(self))

class Quit(Exception):
    '''Raise this to quit the thread run() loop'''
    pass
