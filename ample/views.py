from asciimatics.widgets import Frame, Layout, Label, Button, MultiColumnListBox, Text
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
        layout = Layout([100])
        self.add_layout(layout)
        self.status_label = Label('Not Connected')
        layout.add_widget(self.status_label)
        self.emails = MultiColumnListBox(
            screen.height - 10, ['<50%', '<50%'], self.model.unread_options,
            name='emails'
        )
        layout.add_widget(self.emails)
        layout.add_widget(Button('Reload', self.reload_click))
        layout.add_widget(Button('Logout', self.logout_click))
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


def scenes(screen, inbox):
    if not hasattr(scenes, '_scenes') or scenes.screen != screen:
        setattr(scenes, 'screen', screen)
        views = {}
        for view in [
            LoginView(screen, inbox),
            MainView(screen, inbox)
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
