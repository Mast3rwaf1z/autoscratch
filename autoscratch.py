from include.PackageManager import PackageManager
from include.Package import Package
from include.Database import Database
from os import geteuid
from subprocess import check_output

from include.Logger import warning
from include.Arguments import dbFile, mode, installTarget, uninstallTarget, quiet, searchTarget

if not geteuid() == 0:
    print("\033[38;2;255;0;0mERROR:\033[0m You are not root!")
    exit(1)

Database.initialize(dbFile)

packageManager = PackageManager()

match mode:
    case "install":
        try:
            targets = Package(installTarget).generateList()
            print(f"targets({len(targets)}): ", end="")
            for target in targets: print(f'{Package(target).name}\t', end="")
            if not input("\nProceed with installation? [Y/n]: ").lower() == "y": exit(0)
            timings = {Package(package):packageManager.install(Package(package)) for package in Package(installTarget).generateList()}
            print("-"*10)
            print("Stats")
            for key in timings.keys():
                print(f"Statistics for package {key.name}")
                print(f"\tConfigure:    {timings[key]['configure']}")
                print(f"\tBuild:        {timings[key]['build']}")
                print(f"\tInstall:      {timings[key]['install']}")
        except KeyboardInterrupt as e:
            if not quiet: raise e
            warning("\nInterrupted installer")
    case "uninstall":
        packageManager.uninstall(Package(uninstallTarget))
    case "clean":
        packageManager.clean()
    case "help":
        pass

    case "list":
        Database.print()
    
    case "search":
        files = check_output(["find", "./pkgs", "-name", f"*{searchTarget}*"]).decode()
        print(files)
