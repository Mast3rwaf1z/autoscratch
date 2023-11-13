from subprocess import check_call

from include.Package import Package
from include.Database import Database
from include.Logger import info, error, ok

class PackageManager:
    def install(self, package:Package):
        if not package.name in Database.singleton:
            Database.add(package)
        
        if not package.reinstall and Database.getPackage(package)["configured"]:
            info(f"{package.name} is already configured")
        elif not package.configure():
            info(f"Successfully configured {package.name}")
            Database.update(package, "configured", True)
        else:
            error(f"Failed to configure {package.name}")

        if not package.reinstall and Database.getPackage(package)["built"]:
            info(f"{package.name} is already built")
        elif not package.build():
            info(f"Successfully built {package.name}")
            Database.update(package, "built", True)
        else:
            error(f"Failed to build {package.name}")

        if not package.reinstall and Database.getPackage(package)["installed"]:
            info(f"{package.name} is already installed")
        elif not package.install():
            ok(f"Successfully installed {package.name}")
            Database.update(package, "installed", True)
        else:
            error(f"Failed to install {package.name}")

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