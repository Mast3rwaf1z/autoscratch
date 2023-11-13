from include.Package import Package
from include.Database import Database
from include.Logger import info, error

class PackageManager:
    def install(self, package:Package):
        if not package in Database:
            Database.add(package)

        if not package.configure():
            info(f"Successfully configured {package.name}")
            Database.update(package, "configured", True)
        else:
            error(f"Failed to configure {package.name}")
        if not package.build():
            info(f"Successfully built {package.name}")
            Database.update(package, "built", True)
        else:
            error(f"Failed to build {package.name}")
        if not package.install():
            info(f"Successfully installed {package.name}")
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
            info(f"Successfully uninstalled {package.name}")
            Database.update(package, "installed", False)

