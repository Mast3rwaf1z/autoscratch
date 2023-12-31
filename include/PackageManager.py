from subprocess import check_call
from threading import Thread
from time import sleep, time

from include.Package import Package
from include.Database import Database
from include.Logger import info, error, ok
from include.Arguments import quiet, reinstall

statusMessage = ""
shouldPrint = False

def loading():
    global statusMessage, shouldPrint
    counter = 0
    chars = ["|", "/", "-", "\\"]
    start = now = time()
    while True:
        sleep(.5)
        if shouldPrint: print(f'\r{chars[counter]} | {int(now-start)}s | {statusMessage}\033[0K', end="")
        counter = counter + 1 if counter < (len(chars)-1) else 0
        now = time()

class PackageManager:
    def __init__(self):
        if quiet:
            self.loader = Thread(target=loading, daemon=True)
            self.loader.start()

    def install(self, package:Package) -> dict[str, float]:
        global statusMessage, shouldPrint
        if not package.name in Database.allPackages:
            Database.add(package)

        shouldPrint = True
        timings = {}
        then = time()
        statusMessage = f"Configuring {package.name}..."
        if not package.reinstall and not reinstall and Database.getPackage(package)["configured"]:
            info(f"{package.name} is already configured")
        elif not package.configure():
            info(f"Successfully configured {package.name}")
            Database.update(package, "configured", True)
        else:
            error(f"Failed to configure {package.name}")
        timings["configure"] = time() - then

        then = time()
        statusMessage = f"Building {package.name}..."
        if not package.reinstall and not reinstall and Database.getPackage(package)["built"]:
            info(f"{package.name} is already built")
        elif not package.build():
            info(f"Successfully built {package.name}")
            Database.update(package, "built", True)
        else:
            error(f"Failed to build {package.name}")
        timings["build"] = time() - then

        then = time()
        statusMessage = f"Installing {package.name}..."
        if not package.reinstall and not reinstall and Database.getPackage(package)["installed"]:
            info(f"{package.name} is already installed")
        elif not package.install():
            ok(f"Successfully installed {package.name}")
            Database.update(package, "installed", True)
        else:
            error(f"Failed to install {package.name}")
        timings["install"] = time() - then
        shouldPrint = False

        return timings

    def uninstall(self, package:Package):
        if not package.name in Database.allPackages:
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
        for package in Database.getAll():
            Database.update(package["name"], "configured", False)
            Database.update(package["name"], "built", False)

    def generatePackageList(self, initial:Package):
        info(initial.name)
        packages = list(dict.fromkeys(sum([self.generatePackageList(Package(package)) for package in initial.dependencies if not Package(package).name in Database.installed], []))) + [initial.path]
        info(f"leaving {initial.name}")
        return packages
