import sys


def warn(msg):
    print('Warning: ' + msg, file=sys.stdout)


def abort(msg):
    print('ERROR: ' + msg, file=sys.stderr)
    raise SystemExit(1)
