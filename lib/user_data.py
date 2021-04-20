from pathlib import Path
import os

class UserData:
    def __init__(self, path: Path):
        self.path = path

    def create(
        self,
        password: str,
        pubkey: Path,
        nameservers=None,
        ssh_pwauth=False,
        package_update = None,
        packages = None):
        cloud_config = TEMPLATE.format(
            password=password,
            ssh_pwauth=ssh_pwauth,
            pubkey=pubkey.read_text().strip()
        )
        files = []

        if nameservers:
            files.append("\n".join([
                "- content: |",
            ] + [
               f"    nameserver {nameserver}" for nameserver in nameservers
            ] + [
                "    options edns0",
                "  path: /etc/resolv.conf",
                "  owner: root:root",
                "  permissions: '0777'",
                ""
            ]))

        if len(files) > 0:
            cloud_config += "write_files:\n"
            for file in files:
                cloud_config += file


        if package_update:
            cloud_config += "package_update: true\n"

        if packages:
            cloud_config += "packages:\n"
            for package in packages:
                cloud_config += f" - {package}"

        self.path.write_text(cloud_config)
        return self
    
    def delete(self):
        if self.path.exists():
            os.remove(self.path)
        return self


TEMPLATE = """#cloud-config
password: {password}
chpasswd: {{expire: False}}
ssh_pwauth: {ssh_pwauth}
ssh_authorized_keys:
    - {pubkey}
"""