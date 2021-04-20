from lib.util import shell
import subprocess

class Bridge:
    def __init__(self, name: str):
        self.name = name
    
    def __create(self):
        shell(f"sudo ip link add {self.name} type bridge")

    def __delete(self):
        shell(f"sudo ip link del {self.name}")

    def __set_ip(self, ip):
        shell(f"sudo ip addr add dev {self.name} {ip}")
    
    def __up(self):
        shell(f"sudo ip link set {self.name} up")
    
    def setup(self, ip, nat=True):
        self.__create()
        self.__set_ip(ip)
        self.__up()
        return self
    
    def teardown(self):
        self.__delete()
        return self

