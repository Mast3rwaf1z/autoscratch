from include.PackageManager import PackageManager
from include.Package import Package
from include.Database import Database
from sys import argv
from os import geteuid

if not geteuid() == 0:
    print("\033[38;2;255;0;0mERROR:\033[0m You are not root!")
    exit(1)

Database.initialize(argv[argv.index("--db")+1] if "--db" in argv else "db.db3")

packageManager = PackageManager()

match argv[1]:
    case "install":
        packageManager.install(Package(argv[argv.index("install")+1]))
    case "orderfile":
        with open(argv[argv.index("orderfile")+1], "r") as file:
            for package in file.read().split("\n"):
                packageManager.install(Package(package))