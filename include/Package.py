from json import loads
from subprocess import check_call, DEVNULL, CalledProcessError
from sys import argv

from include.Arguments import quiet


def process(cmd, stderr=None, stdout=None):
    try:
        return check_call(cmd, stderr=stderr, stdout=stdout)
    except CalledProcessError:
        return 1
    
class Package:
    name:str = ""
    src:str | list[str] | None = ""
    configPhase:list[str] = []
    buildPhase:list[str] = []
    installPhase:list[str] = []
    uninstallPhase:list[str] = []

    def __init__(self, filepath:str) -> None:
        if "reinstall" in filepath.lower():
            self.reinstall = True
            filepath = filepath[:filepath.lower().index("reinstall")]+filepath[filepath.lower().index("reinstall")+len("reinstall"):].strip()
        else:
            self.reinstall = False
        with open(filepath, "r") as file:
            config = loads(file.read())

        self.path = filepath
        self.name = config["name"]
        self.src = config["src"]
        self.configPhase = config["config"] if "config" in config else []
        self.buildPhase = config["build"] if "build" in config else []
        self.installPhase = config["install"]
        self.uninstallPhase = config["uninstall"] if "uninstall" in config else []
        self.dependencies = config["depends"] if "depends" in config else []

    def configure(self):
        filename = f"/tmp/{self.name}-config.sh"
        check_call(["rm", "-f", filename])
        check_call(["rm", "-rf", f'build/{self.name}'])
        if not self.src == None: check_call(["rm", "-f", f'build/{self.src.split("/")[-1]}']) if not isinstance(self.src, list) else [check_call(["rm", "-f", f'build/{src.split("/")[-1]}']) for src in self.src]
        with open(filename, "a") as file:
            file.write("source /etc/profile\n")
            file.write("cd build\n")
            if not self.src:
                file.write(f"mkdir -p '{self.name}'\n")
            elif isinstance(self.src, list):
                for src in self.src:
                    file.write(f"wget {src}\n")
                file.write(f"tar xf {self.src[0].split('/')[-1]}\n" if "tar" in self.src[0] or "tgz" in self.src[0] else f"mkdir -p {self.name}\nunzip {self.src[0].split('/')[-1]} -d {self.name}\n")
            else:
                file.write(f"wget {self.src}\n")
                file.write(f"tar xf {self.src.split('/')[-1]}\n" if "tar" in self.src or "tgz" in self.src else f"mkdir -p {self.name}\nunzip {self.src.split('/')[-1]} -d {self.name}\n")
            file.write(f"cd '{self.name}'\n")
            for line in self.configPhase:
                file.write(f"{line}\n")
        
        return process(["bash", filename], stdout=DEVNULL if quiet else None, stderr=DEVNULL if quiet else None)
    
    def build(self):
        filename = f"/tmp/{self.name}-build.sh"
        check_call(["rm", "-f", filename])
        with open(filename, "a") as file:
            file.write("source /etc/profile\n")
            file.write(f"cd build/'{self.name}'\n")
            for line in self.buildPhase:
                file.write(f"{line}\n")

        return process(["bash", filename], stdout=DEVNULL if quiet else None, stderr=DEVNULL if quiet else None)
    
    def install(self):
        filename = f"/tmp/{self.name}-install.sh"
        check_call(["rm", "-f", filename])
        with open(filename, "a") as file:
            file.write("source /etc/profile\n")
            file.write(f"cd build/'{self.name}'\n")
            for line in self.installPhase:
                file.write(f"{line}\n")

        return process(["bash", filename], stdout=DEVNULL if quiet else None, stderr=DEVNULL if quiet else None)
    
    def uninstall(self):
        filename = f"/tmp/{self.name}-uninstall.sh"
        check_call(["rm", "-f", filename])
        with open(filename, "a") as file:
            file.write("source /etc/profile\n")
            file.write(f"cd build/'{self.name}'\n")
            for line in self.uninstallPhase:
                file.write(f"{line}\n")

        return process(["bash", filename], stdout=DEVNULL if quiet else None, stdin=DEVNULL if quiet else None)
