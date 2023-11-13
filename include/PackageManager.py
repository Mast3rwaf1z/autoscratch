from subprocess import check_call
from threading import Thread
from time import sleep
from sys import argv

from include.Package import Package
from include.Database import Database
from include.Logger import info, error, ok

statusMessage = ""
stopLoading = False

def loading():
    global statusMessage, stopLoading
    counter = 0
    chars = [0x2801, 0x2802, 0x2804, 0x2840, 0x2880, 0x2820, 0x2810, 0x2808]
    while not stopLoading:
        sleep(.5)
        print(f'{chr(chars[counter])} | {statusMessage}\033[0K', end="\r")
        counter = counter + 1 if counter < 7 else 0

class PackageManager:
    def install(self, package:Package):
        global statusMessage, stopLoading

        if not package.name in Database.singleton:
            Database.add(package)

        if "--quiet" in argv:
            stopLoading = False
            thread = Thread(target=loading, daemon=True)
            thread.start()
        
        statusMessage = f"Configuring {package.name}..."
        if not package.reinstall and Database.getPackage(package)["configured"]:
            info(f"{package.name} is already configured")
        elif not package.configure():
            info(f"Successfully configured {package.name}")
            Database.update(package, "configured", True)
        else:
            error(f"Failed to configure {package.name}")

        statusMessage = f"Building {package.name}..."
        if not package.reinstall and Database.getPackage(package)["built"]:
            info(f"{package.name} is already built")
        elif not package.build():
            info(f"Successfully built {package.name}")
            Database.update(package, "built", True)
        else:
            error(f"Failed to build {package.name}")

        statusMessage = f"Installing {package.name}..."
        if not package.reinstall and Database.getPackage(package)["installed"]:
            info(f"{package.name} is already installed")
        elif not package.install():
            ok(f"Successfully installed {package.name}")
            Database.update(package, "installed", True)
        else:
            error(f"Failed to install {package.name}")

        if "--quiet" in argv:
            stopLoading = True

    def uninstall(self, package:Package):
        if not package in Database:
            Database.add(package)

        if not package.configure():
            info(f"Successfully configured {package.name}")
            Database.update(package, "configured", True)
        else:
            error(f"Failed to configure {package.name}")

        if not package.uninstall():
            ok(f"Successfully uninstalled {package.name}")
            Database.update(package, "installed", False)

    def clean(self):
        info("Cleaning build directory")
        check_call(["rm", "-rf", "build"])
        check_call(["mkdir", "-p", "build"])