import atexit
import sys
from imbox import Imbox

assert sys.version_info >= (3, 0)


class InboxModel(object):
    def __init__(self):
        self.handle = None
        atexit.register(self.logout)

    def login(self, *args, **kwds):
        self.handle = Imbox(*args, **kwds)

    def logout(self):
        if self.handle is not None:
            try:
                self.handle.logout()
            finally:
                self.handle = None

    @property
    def connected(self):
        return self.handle is not None

    @property
    def unread(self):
        return iter(()) if self.handle is None else self.handle.messages(unread=True)

    @property
    def unread_options(self):
        options = []
        for uid, email in self.unread:
            sent_from = ', '.join([x['name'] for x in email.sent_from])
            options.append(([sent_from, email.subject], int(uid)))

        return options
