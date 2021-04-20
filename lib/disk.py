from pathlib import Path
from lib.user_data import UserData
from lib.network_config import NetworkConfig
from lib.util import shell
import shutil, os, subprocess

class Disk:
    def __init__(self, path: Path):
        self.path = path
    
    def __copy_img(self, base_img):
        shutil.copyfile(base_img, self.path)

    def __resize(self, size: int):
        shell(f"qemu-img resize {self.path} {size}G")
    
    def create_from_base_img(self, base_img: Path, size: int):
        """
        size in GB
        """
        self.__copy_img(base_img=base_img)
        self.__resize(size=size)
        return self

    def create_with_cloud_localds(self, user_data: UserData, network_config: NetworkConfig):
        shell(f"cloud-localds {self.path} {user_data.path} -N {network_config.path}")
        return self
    
    def delete(self):
        if self.path.exists():
            os.remove(self.path)
