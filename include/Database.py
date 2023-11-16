from subprocess import check_call, DEVNULL, check_output
from sys import argv
from json import loads

from include.Package import Package
from include.Logger import info
from include.Arguments import quiet

class listContainer:
    def __init__(self, field):
        self.generator = lambda: [row[field] for row in Database.getAll()]

    def __iter__(self):
        self.value = self.generator()
        self.__i__ = 0
        return self
    def __next__(self):
        if self.__i__ == len(self.value):
            raise StopIteration
        value = self.value[self.__i__]
        self.__i__ += 1
        return value


class Database:
    path:str = ""
    singleton = None
    installed = listContainer("installed")
    built = listContainer("built")
    configured = listContainer("configured")

    def initialize(filepath="/opt/autoscratch/db.db3"):
        info("Initializing database singleton")
        Database.singleton = Database(filepath)


    def __init__(self, filepath) -> None:
        Database.path = filepath
        check_call(
            [
                "sqlite3", 
                Database.path, 
                "create table if not exists packages (name VARCHAR PRIMARY KEY, configured BOOL, built BOOL, installed BOOL)"], 
            stderr=DEVNULL if quiet else None, 
            stdout=DEVNULL if quiet else None)
        
    def add(package:Package):
        if not Database.singleton: Database.initialize()
        return check_call(
            [
                "sqlite3",
                Database.path,
                f"insert into packages values('{package.name}', false, false, false)"
            ], 
            stderr=DEVNULL if quiet else None, 
            stdout=DEVNULL if quiet else None)
    def addTiming(package:Package, type:str, value:float):
        if not Database.singleton: Database.initialize()
        check_call(
            [
                "sqlite3",
                Database.path,
                f"create table if not exists {package.name} (type VARCHAR, value FLOAT)"
            ], 
            stderr=DEVNULL if quiet else None, 
            stdout=DEVNULL if quiet else None)
        check_call(
            [
                "sqlite3",
                Database.path,
                f"insert into {package.name} values('{type}', {value})"
            ], 
            stderr=DEVNULL if quiet else None, 
            stdout=DEVNULL if quiet else None)
    
    def update(package:Package | str, field:str, value:bool):
        if not Database.singleton: Database.initialize()
        return check_call(
            [
                "sqlite3",
                Database.path,
                f"update packages set {field} = {'true' if value else 'false'} where name = '{package.name if isinstance(package, Package) else package}'"
            ]
        )
    
    def getPackage(package:Package) -> dict[str, str | bool]:
        if not Database.singleton: Database.initialize()
        data = loads(check_output(
            [
                "sqlite3",
                Database.path,
                f"select * from packages where name = '{package.name}'",
                "-json"
            ]
        ).decode())
        return data[0]
    def getAll():
        if not Database.singleton: Database.initialize()
        return loads(check_output(
            [
                "sqlite3",
                Database.path,
                f"select * from packages",
                "-json"
            ]
        )) if not len(check_output(["sqlite3", Database.path, "select name from packages"]).decode()) == 0 else []
    
    def print():
        if not Database.singleton: Database.initialize()
        print(check_output([
            "sqlite3",
            Database.path,
            "select * from packages",
            "-table"
        ]).decode())