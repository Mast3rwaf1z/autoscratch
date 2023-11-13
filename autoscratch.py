from include.PackageManager import PackageManager
from include.Package import Package
from include.Database import Database
from sys import argv
from os import geteuid

if not geteuid() == 0:
    print("\033[38;2;255;0;0mERROR:\033[0m You are not root!")
    exit(1)

Database.initialize(argv[argv.index("--db")+1] if "--db" in argv else "db_new.db3")

packageManager = PackageManager()

match argv[1]:
    case "install":
        if "--list" in argv:
            with open(argv[argv.index("--list")+1], "r") as file:
                timings = {Package(package).name:packageManager.install(Package(package)) for package in file.read().split("\n")}
        else:
            timings = {Package(argv[argv.index("install")+1]):packageManager.install(Package(argv[argv.index("install")+1]))}
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