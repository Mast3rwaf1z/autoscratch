from sys import argv
from subprocess import check_output
from json import loads
from os import geteuid, system

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
    print(f'\033[38;2;100;100;100m{msg}\033[0m')

def pkg_install(pkg_name, pkg_cmds):
    print(f'executing install phase for package {pkg_name}')
    tmp_script = f'/tmp/{pkg_name}.pkgmgr'
    if not system(f"rm -f '{tmp_script}'"):
        ok("removed temp script")
    else:
        warning("Failed to remove temp script")
    if not system(f"touch '{tmp_script}'"):
        ok("Created temp file")
    else:
        error(f"Failed to create file: {tmp_script}")
    with open(tmp_script, "a") as file:
        for cmd in pkg_cmds:
            info(f"writing command: {cmd}")
            file.write(f"{cmd}\n")
    if not system(f"bash '{tmp_script}'"):
        ok(f"Successfully installed {pkg_name}")
    else:
        error(f"Failed to install {pkg_name}")

match argv[1]:
    case "single":
        FILENAME = argv[-1]
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
                f"wget {pkg_src} -O build/{pkg_src.split('/')[-1]}", 
                "cd build", 
                json["decomp"] if "decomp" in json else f"tar xf {pkg_src.split('/')[-1]}", 
                f"cd {pkg_name}"
            ] + json["cmds"]
        else:
            pkg_cmds = json["cmds"]
        info(f"beginning build+install phase for package: {pkg_name}")
        pkg_install(pkg_name, pkg_cmds)

    case "orderfile":
        ORDERFILE = argv[-1]
        info(f"reading file: {ORDERFILE}")
        with open(ORDERFILE, "r") as file:
            pkgs = file.read().split("\n")
        for pkg in pkgs:
            info(f"reading file: {pkg}")
            with open(pkg, "r") as file:
                json = loads(file.read())
            pkg_name:str = json["name"]
            pkg_src:str = json["src"]
            info(f"beginning configuration of package: {pkg_name}")
            if pkg_src:
                pkg_cmds:list[str] = [
                    "rm build",
                    "mkdir build",
                    f"wget {pkg_src} -O build/{pkg_src.split('/')[-1]}",
                    "cd build",
                    f"rm -f {pkg_name}",
                    json["decomp"] if "decomp" in json else f"tar xf {pkg_src.split('/')[-1]}",
                    f'cd {pkg_name}'
                ] + json["cmds"]
            else:
                pkg_cmds = json["cmds"]
            info(f"beginning build+install phase for package: {pkg_name}")
            pkg_install(pkg_name, pkg_cmds)


