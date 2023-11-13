from json import loads
from subprocess import check_call, DEVNULL
from sys import argv

class Package:
    name:str = ""
    src:str | list[str] | None = ""
    configPhase:list[str] = []
    buildPhase:list[str] = []
    installPhase:list[str] = []
    uninstallPhase:list[str] = []

    def __init__(self, filepath) -> None:
        with open(filepath, "r") as file:
            config = loads(file.read())

        self.name = config["name"]
        self.src = config["src"]
        self.configPhase = config["config"]
        self.buildPhase = config["build"]
        self.installPhase = config["install"]
        self.uninstallPhase = config["uninstall"]

    def configure(self):
        filename = f"/tmp/{self.name}-config.sh"
        check_call(["rm", "-f", filename])
        with open(filename, "a") as file:
            file.write("cd build\n")
            if isinstance(self.src, list):
                for src in self.src:
                    file.write(f"wget {src}\n")
            else:
                file.write(f"wget {self.src}\n")
            if self.src: file.write(f"tar xf {self.src.split('/')[-1]}\n")
            else: file.write(f"mkdir -p {self.name}\n")
            file.write(f"cd {self.name}\n")
            for line in self.configPhase:
                file.write(f"{line}\n")
        
        return check_call(["bash", filename], stdout=DEVNULL, stderr=DEVNULL)
    
    def build(self):
        filename = f"/tmp/{self.name}-build.sh"
        check_call(["rm", "-f", filename])
        with open(filename, "a") as file:
            file.write(f"cd build/{self.name}\n")
            for line in self.buildPhase:
                file.write(f"{line}\n")

        return check_call(["bash", filename], stdout=DEVNULL if "--quiet" in argv else None, stdin=DEVNULL if "--quiet" in argv else None)
    
    def install(self):
        filename = f"/tmp/{self.name}-install.sh"
        check_call(["rm", "-f", filename])
        with open(filename, "a") as file:
            file.write(f"cd build/{self.name}\n")
            for line in self.installPhase:
                file.write(f"{line}\n")

        return check_call(["bash", filename], stdout=DEVNULL if "--quiet" in argv else None, stdin=DEVNULL if "--quiet" in argv else None)
    
    def uninstall(self):
        filename = f"/tmp/{self.name}-uninstall.sh"
        check_call(["rm", "-f", filename])
        with open(filename, "a") as file:
            file.write(f"cd build/{self.name}\n")
            for line in self.uninstallPhase:
                file.write(f"{line}\n")

        return check_call(["bash", filename], stdout=DEVNULL if "--quiet" in argv else None, stdin=DEVNULL if "--quiet" in argv else None)