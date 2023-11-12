from sys import argv
from subprocess import check_output, check_call, DEVNULL
from json import loads
from os import geteuid, system
from multiprocessing import Process
from time import sleep

indexing = False
quiet = "--quiet" in argv

if not geteuid() == 0:
    print("\033[38;2;255;0;0mERROR:\033[0m You are not root!")
    exit(1)


def ok(msg):
    print(f'\033[38;2;0;255;0m{msg}\033[0m')

def warning(msg):
    print(f'\033[38;2;255;255;0m{msg}\033[0m')

def error(msg):
    print(f'\033[38;2;255;0;0m{msg}\033[0m')
    exit(1)

def info(msg):
    if not quiet: print(f'\033[38;2;100;100;100m{msg}\033[0m')




def loading_icon(package):
    counter = 0
    chars = [0x2801, 0x2802, 0x2804, 0x2840, 0x2880, 0x2820, 0x2810, 0x2808]
    print(f" | Installing {package}...", end="\r")
    while True:
        sleep(.5)
        print(chr(chars[counter]), end="\r")
        counter = counter + 1 if counter < 7 else 0


def run_cmd(cmd, pkg):
    if quiet:
        p = Process(target=loading_icon, args=[pkg])
        p.start()
        return_code = check_call(cmd, stdout=DEVNULL, stderr=DEVNULL)
        p.terminate()
        return return_code
    else:
        return check_call(cmd)

def init_db():
    global indexing
    if not check_call(["sqlite3", "db.db3", "CREATE TABLE IF NOT EXISTS packages (name VARCHAR PRIMARY KEY)"]):
        info("Successfully initialized database")
    else:
        warning("failed to initialize database, disabling indexing")
        indexing = False

def add_package(package):
    if not check_call(['sqlite3', 'db.db3', f"insert or replace into packages values (\'{package}\')"]):
        info("successfully added package to database")
    else:
        warning(f"Failed to add package to database: {package}")

def check_installed(package):
    return len(check_output(["sqlite3", "db.db3", f"select * from packages where name = '{package}'"]).decode().split("\n")) == 1


def pkg_install(pkg_name, pkg_cmds):
    info(f"beginning build+install phase for package: {pkg_name}")
    tmp_script = f'/tmp/{pkg_name}.pkgmgr'
    if not check_call(["rm", "-f" , tmp_script]):
        info("removed temp script")
    else:
        warning("Failed to remove temp script")
    if not check_call(["touch", tmp_script]):
        info("Created temp file")
    else:
        error(f"Failed to create file: {tmp_script}")
    with open(tmp_script, "a") as file:
        for cmd in pkg_cmds:
            info(f"writing command: {cmd}")
            file.write(f"{cmd}\n")
    if not run_cmd(["bash", tmp_script], pkg_name):
        ok(f"Successfully installed {pkg_name}")
        if indexing: add_package(pkg_name)
    else:
        error(f"Failed to install {pkg_name}")

def pkg_configure(FILENAME):
    info(f"reading file: {FILENAME}")
    with open(FILENAME, "r") as file:
        json = loads(file.read())
    pkg_name:str = json["name"]
    pkg_src:str = json["src"]
    info(f"beginning configuration of package: {pkg_name}")
    #print(type(pkg_src))
    if pkg_src:
        pkg_cmds:list[str] = [
            "rm build", 
            "mkdir build", 
            "\n".join([f"wget {pkg} -O build/{pkg.split('/')[-1]}" for pkg in pkg_src]) if isinstance(pkg_src, list) else f"wget {pkg_src} -O build/{pkg_src.split('/')[-1]}", 
            "cd build", 
            json["decomp"] if "decomp" in json else f"tar xf {pkg_src[0].split('/')[-1]}" if isinstance(pkg_src, list) else f"tar xf {pkg_src.split('/')[-1]}", 
            f"cd {pkg_name}"
        ] + json["cmds"]
    else:
        pkg_cmds = json["cmds"]
    return pkg_name, pkg_cmds

if __name__ == "__main__":
    if not check_call(["rm", "-rf", "build"], stdout=DEVNULL):
        info("successfully cleaned build environment")
    else:
        warning("Failed to clear build environment")

    if not "--nowhich" in argv and not check_call(["which", "sqlite3"], stdout=DEVNULL):
        info("Sqlite3 installation found!")
        indexing = True
    else:
        warning("Sqlite3 not found, disabling package indexing")
        indexing = False
    if indexing: 
        init_db()

    match argv[1]:
        case "single":
            FILENAME = argv[-1]
            pkg_name, pkg_cmds = pkg_configure(FILENAME)
            pkg_install(pkg_name, pkg_cmds)

        case "orderfile":
            ORDERFILE = argv[-1]
            info(f"reading file: {ORDERFILE}")
            with open(ORDERFILE, "r") as file:
                pkgs = file.read().split("\n")
            for pkg in pkgs:
                reinstall = "reinstall" in pkg.lower()
                pkg = pkg.split(" ")[1] if "reinstall" in pkg.lower() else pkg
                pkg_name, pkg_cmds = pkg_configure(pkg)
                if not check_installed(pkg_name) and not reinstall: 
                    info(f"Package {pkg_name} is already installed!")
                else:
                    pkg_install(pkg_name, pkg_cmds)
        case "list":
            print(check_output(["sqlite3", "db.db3", "select * from packages", "-table"]).decode())