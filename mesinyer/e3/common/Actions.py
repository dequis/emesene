import Queue

import e3

class Actions(Queue.Queue):
    '''A queue that turns calls to attributes into action puts
    For example:
        queue.action(argument, key='word')
    would do
        queue.put(('action', (argument, ), {'key': 'word'}))
    '''
    def __getattr__(self, attr):
        if attr.startswith("_"):
            return Queue.Queue.__getattr__(self, attr)
        else:
            def f(*args, **kwds):
                self.put((attr, args, kwds))
            return f
