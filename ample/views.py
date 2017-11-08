from asciimatics.widgets import Frame, Layout, Label, Button, MultiColumnListBox, Text, Divider, TextBox
from asciimatics.scene import Scene
from asciimatics.exceptions import StopApplication, NextScene
import json
import os


class LoginView(Frame):
    def __init__(self, screen, model):
        super(LoginView, self).__init__(
            screen,
            10,
            50,
            has_shadow=True,
            name='Login',
            reduce_cpu=True
        )
        self.model = model
        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Text('Host:', 'host'))
        layout.add_widget(Text('Email:', 'email'))
        layout.add_widget(Text('Pasword:', 'password', hide_char='*'))
        layout.add_widget(Button('Login', self.login_click))
        layout.add_widget(Button('Cancel', self.cancel_click))
        self.fix()
        self.cfg_path = os.path.expanduser('~/.ample')
        if os.path.exists(self.cfg_path):
            with open(self.cfg_path, 'r') as f:
                self.data = json.load(f)

    @staticmethod
    def cancel_click():
        raise StopApplication('Quit')

    def login_click(self):
        self.save()
        try:
            self.model.login(
                self.data['host'],
                username=self.data['email'],
                password=self.data['password'],
                ssl=True,
                ssl_context=None
            )
        except Exception as ex:
            raise StopApplication(str(ex))

        with open(self.cfg_path, 'w') as f:
            f.write(json.dumps(self.data))

        view('MainView').reload_click()
        open_view('MainView')


class MainView(Frame):
    def __init__(self, screen, model):
        super(MainView, self).__init__(
            screen,
            screen.height,
            screen.width,
            has_shadow=True,
            name='Main View'
        )
        self.model = model
        status_layout = Layout([80, 10, 10])
        self.add_layout(status_layout)
        self.status_label = Label('Not Connected')
        status_layout.add_widget(
            self.status_label,
            column=0
        )
        status_layout.add_widget(
            Button('Reload', self.reload_click),
            column=1
        )
        status_layout.add_widget(
            Button('Logout', self.logout_click),
            column=2
        )
        layout = Layout([100])
        self.add_layout(layout)
        self.emails = MultiColumnListBox(
            screen.height - 10, ['<50%', '<50%'], self.model.unread_options,
            name='emails',
            on_select=self.select_email
        )
        layout.add_widget(self.emails)
        self.fix()

    def reload_click(self):
        self.save()
        options = self.model.unread_options
        if self.model.connected:
            self.status_label._text = 'Unread: %s' % (len(options))
            self.emails.options = options

        else:
            self.status_label._text = 'Not Connected'
            self.emails.options = []

    @staticmethod
    def logout_click():
        raise StopApplication('Logout')

    def select_email(self):
        uid = self.emails.value
        view('EmailView').open(uid)


class EmailView(Frame):
    def __init__(self, screen, model):
        super(EmailView, self).__init__(
            screen,
            screen.height,
            screen.width,
            has_shadow=True,
            name='Main View'
        )
        self.data = {
            'subject': '',
            'from': '',
            'to': '',
            'body': '',
            'date': ''
        }
        self.model = model
        self.uid = None
        layout = Layout([10, 80, 80])
        self.add_layout(layout)
        layout.add_widget(
            Button('Back', self.back_click),
            column=0
        )
        layout.add_widget(
            Button('Reply', self.reply_click),
            column=2
        )
        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(self._text('Subject', 'subject'))
        layout.add_widget(self._text('To', 'to'))
        layout.add_widget(self._text('From', 'from'))
        layout.add_widget(self._text('Date', 'date'))
        textbox = TextBox(
            screen.height - 4,
            label='Body',
            name='body',
            as_string=True
        )
        layout.add_widget(textbox)
        self.fix()

    @staticmethod
    def _text(label, name):
        widget = Text(label, name)
        # widget.disabled = True
        return widget

    def open(self, uid):
        self.uid = uid
        email = self.model.get(uid)
        self.data = {
            'subject': email.subject,
            'from': ', '.join([x['name'] for x in email.sent_from]),
            'to': ', '.join([x['name'] for x in email.sent_to]),
            'body': '\n'.join(email.body['plain']),
            'date': email.date
        }
        self.save()
        open_view('EmailView')

    @staticmethod
    def back_click():
        open_view('MainView')

    def reply_click(self):
        view('ReplyView').open(self.uid)


def scenes(screen, inbox):
    if not hasattr(scenes, '_scenes') or scenes.screen != screen:
        setattr(scenes, 'screen', screen)
        views = {}
        for view in [
            LoginView(screen, inbox),
            MainView(screen, inbox),
            EmailView(screen, inbox)
        ]:
            views[view.__class__.__name__] = view

        setattr(scenes, 'views', views)
        _scenes = []
        for name in views.keys():
            _scenes.append(Scene([views[name]], -1, name=name))

        setattr(scenes, '_scenes', _scenes)

    return getattr(scenes, '_scenes')


def view(name):
    if not hasattr(scenes, 'views'):
        return None

    return scenes.views[name]


def open_view(name):
    if view(name) is None:
        raise ValueError('View %s does not exist' % (name))

    raise NextScene(name)
