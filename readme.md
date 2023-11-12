# Autoscratch
This project defines a package manager where all packages are defined locally and stored locally in a database.

# install
it is recommended to use the tool to install which and sqlite3 twice to record them into the database using itself
```sh
python3 autoscratch.py single pkgs/Which-2.21.json
python3 autoscratch.py single pkgs/SQLite-3.42.0.json
```

# usage
there are a few commands defined:
```sh
# this command installs a single package regardless of dependency installation
python3 autoscratch.py single pkgs/<pkgname>-<pkgver>.json
# this command takes a file containing a list of (relative) paths to package configurations, such that packages can be installed in the correct order
python3 autoscratch.py orderfile <orderfile-path>
# lists all installed packages
python3 autoscratch.py list
```