from sys import argv

mode = argv[1]

quiet = not "--verbose" in argv or "-v" in argv

reinstall = "--reinstall" in argv or "-r" in argv

dbFile = argv[argv.index("--db")+1] if "--db" in argv else "db_new.db3"

installTarget = argv[argv.index("install")+1] if "install" in argv else None
uninstallTarget = argv[argv.index("uninstall")+1] if "uninstall" in argv else None
searchTarget = argv[argv.index("search")+1] if "search" in argv else None
ask = not "--noask" in argv