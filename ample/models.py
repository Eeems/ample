import sys
from imbox import Imbox

assert sys.version_info >= (3, 0)


class InboxModel(object):
    def __init__(self):
        self.args = None
        self.kwds = None
        self.connected = False

    def login(self, *args, **kwds):
        self.args = args
        self.kwds = kwds
        with Imbox(*args, **kwds):
            self.connected = True

    def logout(self):
        self.connected = False

    def get(self, uid):
        if not self.connected:
            return None

        with self.handle() as handle:
            res = handle.fetch_by_uid(uid)

        return res

    @property
    def unread(self):
        if not self.connected:
            return iter(())
        with self.handle() as handle:
            res = list(handle.messages(unread=True))

        return res

    @property
    def unread_options(self):
        if not self.connected:
            return iter(())

        options = []
        with self.handle() as handle:
            for uid, email in handle.messages(unread=True):
                sent_from = ', '.join([x['name'] for x in email.sent_from])
                options.append(([sent_from, email.subject], uid))

        return options

    def handle(self):
        if not self.connected:
            raise Exception('Not connected')

        return Imbox(*self.args, **self.kwds)
