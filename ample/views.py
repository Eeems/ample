from asciimatics.widgets import Frame, Layout, Text, Button
from asciimatics.exceptions import StopApplication


class MainView(Frame):
    def __init__(self, screen):
        super(MainView, self).__init__(
            screen,
            5,
            50,
            has_shadow=True,
            name='Main View',
            reduce_cpu=True
        )
        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Text("Name: ", "name"))
        layout.add_widget(Button('Okay', self.okay_click))
        self.fix()

    def okay_click(self):
        raise StopApplication('Quit')
