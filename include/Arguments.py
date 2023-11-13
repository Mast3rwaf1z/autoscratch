from sys import argv

mode = argv[1]

quiet = not "--verbose" in argv or "-v" in argv

listMode = "--list" in argv or "-l" in argv

listFile = argv[argv.index("--list")+1] if "--list" in argv else argv[argv.index("-l")+1] if listMode else None

reinstall = "--reinstall" in argv or "-r" in argv

dbFile = argv[argv.index("--db")+1] if "--db" in argv else "db_new.db3"

installTarget = argv[argv.index("install")+1] if "install" in argv else None