from include.PackageManager import PackageManager
from include.Package import Package
from include.Database import Database
from os import geteuid

from include.Logger import warning
from include.Arguments import dbFile, listFile, listMode, mode, installTarget, uninstallTarget, quiet

if not geteuid() == 0:
    print("\033[38;2;255;0;0mERROR:\033[0m You are not root!")
    exit(1)

Database.initialize(dbFile)

packageManager = PackageManager()

match mode:
    case "install":
        try:
            if listMode:
                with open(listFile, "r") as file:
                    timings = {Package(package):packageManager.install(Package(package)) for package in file.read().split("\n")}
            else:
                timings = {Package(installTarget):packageManager.install(Package(installTarget))}
            print("-"*10)
            print("Stats")
            for key in timings.keys():
                print(f"Statistics for package {key.name}")
                print(f"\tConfigure:    {timings[key]['configure']}")
                print(f"\tBuild:        {timings[key]['build']}")
                print(f"\tInstall:      {timings[key]['install']}")
        except KeyboardInterrupt as e:
            if not quiet: raise e
            warning("Interrupted installer")
    case "uninstall":
        packageManager.uninstall(Package(uninstallTarget))
    case "clean":
        packageManager.clean()
    case "help":
        pass

    case "list":
        Database.print()
