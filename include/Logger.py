from sys import argv

def ok(msg):
    print(f'\033[38;2;0;255;0m{msg}\033[0m')

def warning(msg):
    print(f'\033[38;2;255;255;0m{msg}\033[0m')

def error(msg):
    print(f'\033[38;2;255;0;0m{msg}\033[0m')
    exit(1)

def info(msg):
    if not "--quiet" in argv: print(f'\033[38;2;100;100;100m{msg}\033[0m')