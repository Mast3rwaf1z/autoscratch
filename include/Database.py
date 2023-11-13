from subprocess import check_call, DEVNULL, check_output
from sys import argv
from json import loads

from include.Package import Package
from include.Logger import info

class Database:
    path:str = ""
    singleton = None

    def initialize(filepath="/opt/autoscratch/db.db3"):
        info("Initializing database singleton")
        Database.singleton = Database(filepath)


    def __init__(self, filepath) -> None:
        self.path = filepath
        check_call(
            [
                "sqlite3", 
                "db.db3", 
                "create table if not exists packages (name VARCHAR PRIMARY KEY, configured BOOL, built BOOL, installed BOOL)"], 
            stderr=DEVNULL if "--quiet" in argv else None, 
            stdout=DEVNULL if "--quiet" in argv else None)
        
    def add(package:Package):
        if not Database.singleton: Database.initialize()
        return check_call(
            [
                "sqlite3",
                "db.db3",
                f"insert into packages values('{package.name}', false, false, false)"
            ]
        )
    
    def update(package:Package, field:str, value:bool):
        if not Database.singleton: Database.initialize()
        return check_call(
            [
                "sqlite3",
                "db.db3",
                f"update packages set {field} = {'true' if value else 'false'} where name = '{package.name}'"
            ]
        )
    
    def getPackage(package:Package) -> dict[str, str | bool]:
        if not Database.singleton: Database.initialize()
        data = loads(check_output(
            [
                "sqlite3",
                "db.db3",
                f"select * from packages where name = '{package.name}'",
                "-json"
            ]
        ).decode())
        return data[0]
    def getAll():
        return loads(check_output(
            [
                "sqlite3",
                "db.db3",
                f"select * from packages",
                "-json"
            ]
        )) if not len(check_output(["sqlite3", "db.db3", "select name from packages"]).decode()) == 0 else []
    
    def __iter__(self):
        self.__names__ = [package["name"] for package in Database.getAll()]
        self.__i__ = 0
        return self
    def __next__(self):

        if self.__i__ == len(self.__names__):
            raise StopIteration
        name = self.__names__[self.__i__]
        self.__i__ += 1
        return name
        