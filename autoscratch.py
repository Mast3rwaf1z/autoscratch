from include.PackageManager import PackageManager
from include.Package import Package
from include.Database import Database
from os import geteuid

from include.Arguments import dbFile, listFile, listMode, mode, installTarget

if not geteuid() == 0:
    print("\033[38;2;255;0;0mERROR:\033[0m You are not root!")
    exit(1)

Database.initialize(dbFile)

packageManager = PackageManager()

match mode:
    case "install":
        if listMode:
            with open(listFile, "r") as file:
                timings = {Package(package).name:packageManager.install(Package(package)) for package in file.read().split("\n")}
        else:
            timings = {Package(installTarget):packageManager.install(Package(installTarget))}
        print("-"*10)
        print("Stats")
        for key in timings:
            print(f"Statistics for package {key}")
            print(f"\tConfigure:    {timings['configure']}")
            print(f"\tBuild:        {timings['build']}")
            print(f"\tInstall:      {timings['install']}")
    case "help":
        pass

    case "list":
        Database.print()