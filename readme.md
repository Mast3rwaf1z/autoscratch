# Autoscratch
This project defines a package manager where all packages are defined locally and stored locally in a database.

# install
it is recommended to use the tool to install which and sqlite3 twice to record them into the database using itself
```sh
python3 autoscratch.py install pkgs/blfs/system-utilities/Which-2.21.json
python3 autoscratch.py install pkgs/blfs/databases/SQLite-3.42.0.json
python3 autoscratch.py install pkgs/custom/autoscratch.json
```

# usage
there are a few commands defined:
```sh
# this command installs a single package
autoscratch install <path-to-config>.json
# lists all installed packages
autoscratch list
# searches package definitions for a file, uses `find` under the hood
autoscratch search <search string>
```
