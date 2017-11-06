import sys
from traceback import format_exc
from decopts import entrypoint
from .views import MainView
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError


@entrypoint(
    prog='snake',
    description='Email from the command line',
    add_help=True
)
def main():
    last_scene = None
    while True:
        try:
            Screen.wrapper(view, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene


def view(screen, scene):
    screen.play(
        [Scene([MainView(screen)])],
        stop_on_resize=True,
        start_scene=scene
    )


if __name__ == '__main__':
    try:
        main()

    except Exception:
        print('Error encountered:\n%s' % (format_exc().strip()))
