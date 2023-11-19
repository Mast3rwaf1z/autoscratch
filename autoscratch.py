from include.PackageManager import PackageManager
from include.Package import Package
from include.Database import Database
from os import geteuid, chdir
from subprocess import check_output,check_call, DEVNULL


from include.Logger import warning
from include.Arguments import dbFile, mode, installTarget, uninstallTarget, quiet, searchTarget, ask

def check_root():
    if not geteuid() == 0:
        print("\033[38;2;255;0;0mERROR:\033[0m You are not root!")
        exit(1)

Database.initialize(dbFile)

packageManager = PackageManager()

match mode:
    case "install":
        check_root()
        try:
            targets = packageManager.generatePackageList(Package(installTarget))
            if ask:
                print(f"targets({len(targets)}): ", end="\r\t\t")
                for i, target in enumerate(targets): 
                    if i%5 == 0 and not i == 0: # newline every 5 prints
                        print("\n\t\t", end="")
                    print(f'{Package(target).name} ', end="")
                if not input("\n\nProceed with installation? [Y/n]: ").lower() in ["y", "", "yes"]: exit(0)
            timings = {Package(package):packageManager.install(Package(package)) for package in targets}
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
        check_root()
        packageManager.uninstall(Package(uninstallTarget))
    case "clean":
        check_root()
        packageManager.clean()
    case "help":
        pass

    case "list":
        Database.print()
    
    case "search":
        files = check_output(["find", "./pkgs", "-name", f"*{searchTarget}*"]).decode()
        print(files)
    
    case "update":
        check_root()
        check_call(["rm", "-rf", "/tmp/autoscratch"])
        check_call(["mkdir", "/tmp/autoscratch"])
        chdir("/tmp/autoscratch")
        for call in [
            ["git", "clone", "https://github.com/Mast3rwaf1z/autoscratch.git", "/tmp/autoscratch"],
            ["mkdir", "/tmp/autoscratch/build"],
            ["python3", "autoscratch.py", "install", "pkgs/custom/autoscratch.json", "--reinstall", "--verbose", "--noask"]
        ]:
            check_call(call, stdout=DEVNULL if quiet else None, stderr=DEVNULL if quiet else None)
