from asciimatics.widgets import Widget


class AnsiLabel(Widget):
    def __init__(self, height, name=None, **kwargs):
        super(AnsiLabel, self).__init__(name, **kwargs)
        self._column = 0
        self._required_height = height

    def update(self, frame_no):
        pass

    def reset(self):
        pass

    def process_event(self, event):
        pass

    def required_height(self, offset, width):
        return self._required_height

    @property
    def frame_update_count(self):
        # Force refresh for cursor if needed.
        return 5 if self._has_focus and not self._frame.reduce_cpu else 0
