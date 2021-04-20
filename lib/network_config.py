from pathlib import Path
import os

class NetworkConfig:
    def __init__(self, path: Path):
        self.path = path
    
    def create(self, interfaces: list):
        network_config = TEMPLATE
        for interface in interfaces:
          network_config += INTERFACE.format(
            name=interface["name"],
            mac=interface["mac"],
            address=interface["address"],
            gateway=interface["gateway"],
            dns_server=interface["dns_server"]
          )
        self.path.write_text(network_config)

    def delete(self):
        if self.path.exists():
            os.remove(self.path)

TEMPLATE = """# custom network config
version: 2
ethernets:
"""

INTERFACE = """
  {name}:
    match:
      macaddress: "{mac}"
    set-name: {name}
    addresses:
    - {address}
    dhcp4: false
    gateway4: {gateway}
    nameservers:
      addresses:
      - {dns_server}
"""