import decopts
from traceback import format_exc

@entrypoint(
    prog='snake',
    description='Email from the command line',
    add_help=True
)
def main:
    pass


if __name__ == '__main__':
    try:
        main()

    except Exception:
        print('Error encountered:\n%s' % (format_exc().strip()))
