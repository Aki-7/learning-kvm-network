import subprocess
from paramiko import SSHClient, AutoAddPolicy, Ed25519Key
from paramiko.ssh_exception import NoValidConnectionsError 
from pathlib import Path
from lib.disk import Disk
from lib.bridge import Bridge
from typing import Tuple, List

class VM:
    accessible = False
    def __init__(self, name: str):
        self.name = name
    
    def install(
        self,
        bridges: List[Tuple[Bridge, str]],
        vcpus=1,
        ram=2048,
        os_variant="ubuntu18.04",
        disks: List[Tuple[Disk, str]] = []
    ):
        cmds = [
            "virt-install",
            "--name", self.name,
            "--vcpus", f"{vcpus}",
            "--ram", f"{ram}",
            "--hvm",
            "--virt-type", "kvm",
            "--os-type", "linux",
            "--os-variant", os_variant,
            "--graphics", "none",
            "--serial", "pty",
            "--import",
            "--noreboot",
        ]

        for (bridge, mac) in bridges:
            cmds.append("--network")
            cmds.append(f"bridge={bridge.name},mac={mac}")

        for (disk, opts) in disks:
            cmds.append("--disk")
            if opts:
                cmds.append(f"path=\"{disk.path},{opts}\"")
            else:
                cmds.append(f"path={disk.path}")
        cmd = " ".join(cmds)
        subprocess.run(cmd, shell=True)
        cmd = f"virsh start {self.name}"
        subprocess.run(cmd, shell=True)
        return self
    
    def destroy(self):
        cmd = f"virsh destroy {self.name}"
        subprocess.run(cmd, shell=True)
        cmd = f"virsh undefine --domain {self.name} --wipe-storage --remove-all-storage"
        subprocess.run(cmd, shell=True)
        return self
    
    def set_access_info(self, user: str, host: str, pkey: Path, passphrase: str):
        self.accessible = True
        self.user = user
        self.host = host
        self.pkey = pkey
        self.passphrase = passphrase
    
    def ping(self):
        if self.accessible == False:
            print("No access info...")
            return False
        
        pkey_file = self.pkey.open()
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        try:
            client.connect(
                hostname=self.host,
                pkey=Ed25519Key.from_private_key(pkey_file, self.passphrase),
                passphrase=self.passphrase,
                username=self.user
            )
            print(f"{self.name} is started.", flush=True)
            return True
        except NoValidConnectionsError as e:
            print(e, flush=True)
            return False
