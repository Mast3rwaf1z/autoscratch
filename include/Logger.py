from include.Arguments import quiet

def ok(msg):
    print(f'\r\033[38;2;0;255;0m{msg}\033[0m')

def warning(msg):
    print(f'\033[38;2;255;255;0m{msg}\033[0m')

def error(msg):
    print(f'\033[38;2;255;0;0m{msg}\033[0m')
    exit(1)

def info(msg):
    if not quiet: print(f'\033[38;2;100;100;100m{msg}\033[0m')