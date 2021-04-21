#!python3
from lib.privilege_check import privileged_or_exit
from lib.variables import project_root, working_dir
from lib.bridge import Bridge
from lib.disk import Disk
from lib.nat_rule import NatRule
from lib.direct_rule import DirectRule
from lib.user_data import UserData
from lib.network_config import NetworkConfig
from lib.vm import VM
from argparse import ArgumentParser
from pathlib import Path
import subprocess, time

# variables
base_img = project_root/"img"/"ubuntu-18.04-server-cloudimg-amd64.img"
PASSWORD="ubuntu"
PUB_KEY=Path.home()/".ssh"/"id_ed25519.pub"
PRIV_KEY=Path.home()/".ssh"/"id_ed25519"
PRIV_KEY_PASS=""
DNS_ADDRESS="192.168.0.1"

# bridges
br0 = Bridge("br0")
BR0_ADDRESS_M = "192.168.100.1/24"
BR0_ADDRESS = "192.168.100.1"
BR0_SUBNET = "192.168.100.0/24"
br0_nat_rule = NatRule(br0)

br1 = Bridge("br1")
BR1_ADDRESS_M="192.168.101.1/24"
BR1_ADDRESS="192.168.101.1"
BR1_SUBNET="192.168.101.0/24"
br1_direct_rule = DirectRule(br1)

br2 = Bridge("br2")
BR2_ADDRESS_M="192.168.102.1/24"
BR2_ADDRESS="192.168.102.1"
BR2_SUBNET="192.168.102.0/24"
br2_direct_rule = DirectRule(br2)

br3 = Bridge("br3")
BR3_ADDRESS_M="192.168.103.1/24"
BR3_ADDRESS="192.168.103.1"
BR3_SUBNET="192.168.103.0/24"
br3_direct_rule = DirectRule(br3)

# disks
user_data11 = UserData(path=working_dir/"user-data-11")
network_config11 = NetworkConfig(path=working_dir/"network-config-11")
user_data_disk11 = Disk(path=working_dir/"vm11-user-data.img")
disk11 = Disk(path=working_dir/"vm11.img")

user_data12 = UserData(path=working_dir/"user-data-12")
network_config12 = NetworkConfig(path=working_dir/"network-config-12")
user_data_disk12 = Disk(path=working_dir/"vm12-user-data.img")
disk12 = Disk(path=working_dir/"vm12.img")

user_data13 = UserData(path=working_dir/"user-data-13")
network_config13 = NetworkConfig(path=working_dir/"network-config-13")
user_data_disk13 = Disk(path=working_dir/"vm13-user-data.img")
disk13 = Disk(path=working_dir/"vm13.img")

user_data14 = UserData(path=working_dir/"user-data-14")
network_config14 = NetworkConfig(path=working_dir/"network-config-14")
user_data_disk14 = Disk(path=working_dir/"vm14-user-data.img")
disk14 = Disk(path=working_dir/"vm14.img")

# vms
vm11 = VM("c11")
VM11_BR0_ADDRESS_M="192.168.100.11/24"
VM11_BR0_ADDRESS="192.168.100.11"
VM11_BR0_MAC="52:54:00:00:11:00"
VM11_BR1_ADDRESS_M="192.168.101.11/24"
VM11_BR1_ADDRESS="192.168.101.11"
VM11_BR1_MAC="52:54:00:00:11:01"

vm12 = VM("r12")
VM12_BR0_ADDRESS_M="192.168.100.12/24"
VM12_BR0_ADDRESS="192.168.100.12"
VM12_BR0_MAC="52:54:00:00:12:00"
VM12_BR1_ADDRESS_M="192.168.101.12/24"
VM12_BR1_ADDRESS="192.168.101.12"
VM12_BR1_MAC="52:54:00:00:12:01"
VM12_BR2_ADDRESS_M="192.168.102.12/24"
VM12_BR2_ADDRESS="192.168.102.12"
VM12_BR2_MAC="52:54:00:00:12:02"

vm13 = VM("r13")
VM13_BR0_ADDRESS_M="192.168.100.13/24"
VM13_BR0_ADDRESS="192.168.100.13"
VM13_BR0_MAC="52:54:00:00:13:00"
VM13_BR2_ADDRESS_M="192.168.102.13/24"
VM13_BR2_ADDRESS="192.168.102.13"
VM13_BR2_MAC="52:54:00:00:13:02"
VM13_BR3_ADDRESS_M="192.168.103.13/24"
VM13_BR3_ADDRESS="192.168.103.13"
VM13_BR3_MAC="52:54:00:00:13:03"

vm14 = VM("c14")
VM14_BR0_ADDRESS_M="192.168.100.14/24"
VM14_BR0_ADDRESS="192.168.100.14"
VM14_BR0_MAC="52:54:00:00:14:00"
VM14_BR3_ADDRESS_M="192.168.103.14/24"
VM14_BR3_ADDRESS="192.168.103.14"
VM14_BR3_MAC="52:54:00:00:14:03"

VM11_NETWORK_CONFIG = f"""# custom network config
version: 2
ethernets:
  eth0:
    match:
      macaddress: "{VM11_BR0_MAC}"
    set-name: eth0
    addresses:
    - {VM11_BR0_ADDRESS_M}
    dhcp4: false
    nameservers:
      addresses:
      - {DNS_ADDRESS}
    routes:
    - to: 0.0.0.0/0
      via: {BR0_ADDRESS}

  eth1:
    match:
      macaddress: "{VM11_BR1_MAC}"
    set-name: eth1
    addresses:
    - {VM11_BR1_ADDRESS_M}
    dhcp4: false
    nameservers:
      addresses:
      - {DNS_ADDRESS}
    routes:
    - to: {BR2_SUBNET}
      via: {VM12_BR1_ADDRESS}
    - to: {BR3_SUBNET}
      via: {VM12_BR1_ADDRESS}
"""

VM12_NETWORK_CONFIG = f"""# custom network config
version: 2
ethernets:
  eth0:
    match:
      macaddress: "{VM12_BR0_MAC}"
    set-name: eth0
    addresses:
    - {VM12_BR0_ADDRESS_M}
    dhcp4: false
    nameservers:
      addresses:
      - {DNS_ADDRESS}
    routes:
    - to: 0.0.0.0/0
      via: {BR0_ADDRESS}

  eth1:
    match:
      macaddress: "{VM12_BR1_MAC}"
    set-name: eth1
    addresses:
    - {VM12_BR1_ADDRESS_M}
    dhcp4: false
    nameservers:
      addresses:
      - {DNS_ADDRESS}

  eth2:
    match:
      macaddress: "{VM12_BR2_MAC}"
    set-name: eth2
    addresses:
    - {VM12_BR2_ADDRESS_M}
    dhcp4: false
    nameservers:
      addresses:
      - {DNS_ADDRESS}
"""

VM13_NETWORK_CONFIG = f"""# custom network config
version: 2
ethernets:
  eth0:
    match:
      macaddress: "{VM13_BR0_MAC}"
    set-name: eth0
    addresses:
    - {VM13_BR0_ADDRESS_M}
    dhcp4: false
    nameservers:
      addresses:
      - {DNS_ADDRESS}
    routes:
    - to: 0.0.0.0/0
      via: {BR0_ADDRESS}

  eth1:
    match:
      macaddress: "{VM13_BR2_MAC}"
    set-name: eth1
    addresses:
    - {VM13_BR2_ADDRESS_M}
    dhcp4: false
    nameservers:
      addresses:
      - {DNS_ADDRESS}

  eth2:
    match:
      macaddress: "{VM13_BR3_MAC}"
    set-name: eth2
    addresses:
    - {VM13_BR3_ADDRESS_M}
    dhcp4: false
    nameservers:
      addresses:
      - {DNS_ADDRESS}
"""

VM14_NETWORK_CONFIG = f"""# custom network config
version: 2
ethernets:
  eth0:
    match:
      macaddress: "{VM14_BR0_MAC}"
    set-name: eth0
    addresses:
    - {VM14_BR0_ADDRESS_M}
    dhcp4: false
    nameservers:
      addresses:
      - {DNS_ADDRESS}
    routes:
    - to: 0.0.0.0/0
      via: {BR0_ADDRESS}

  eth1:
    match:
      macaddress: "{VM14_BR3_MAC}"
    set-name: eth1
    addresses:
    - {VM14_BR3_ADDRESS_M}
    dhcp4: false
    nameservers:
      addresses:
      - {DNS_ADDRESS}
    routes:
    - to: {BR1_SUBNET}
      via: {VM13_BR3_ADDRESS}
    - to: {BR2_SUBNET}
      via: {VM13_BR3_ADDRESS}
"""

def setup():
    # bridges
    br0.setup(BR0_ADDRESS_M)
    br0_nat_rule.create(subnet=BR0_SUBNET)

    br1.setup(BR1_ADDRESS_M)
    br1_direct_rule.create()

    br2.setup(BR2_ADDRESS_M)
    br2_direct_rule.create()

    br3.setup(BR3_ADDRESS_M)
    br3_direct_rule.create()

    # vm 11
    disk11.create_from_base_img(base_img, size=10)
    user_data11.create(
        password=PASSWORD,
        pubkey=PUB_KEY,
        nameservers=[DNS_ADDRESS],
        package_update=True
    )
    network_config11.create(VM11_NETWORK_CONFIG)
    user_data_disk11.create_with_cloud_localds(
        user_data=user_data11,
        network_config=network_config11
    )
    vm11.install(
        bridges=[(br0, VM11_BR0_MAC), (br1, VM11_BR1_MAC)],
        disks=[(user_data_disk11, "device=cdrom"), (disk11, "")]
    )

    # vm 12
    disk12.create_from_base_img(base_img, size=10)
    user_data12.create(
        password=PASSWORD,
        pubkey=PUB_KEY,
        nameservers=[DNS_ADDRESS]
    )
    network_config12.create(VM12_NETWORK_CONFIG)
    user_data_disk12.create_with_cloud_localds(
        user_data=user_data12,
        network_config=network_config12
    )
    vm12.install(
        bridges=[(br0, VM12_BR0_MAC), (br1, VM12_BR1_MAC), (br2, VM12_BR2_MAC)],
        disks=[(user_data_disk12, "device=cdrom"), (disk12, "")]
    )

    # vm 13
    disk13.create_from_base_img(base_img, size=10)
    user_data13.create(
        password=PASSWORD,
        pubkey=PUB_KEY,
        nameservers=[DNS_ADDRESS]
    )
    network_config13.create(VM13_NETWORK_CONFIG)
    user_data_disk13.create_with_cloud_localds(
        user_data=user_data13,
        network_config=network_config13
    )
    vm13.install(
        bridges=[(br0, VM13_BR0_MAC), (br2, VM13_BR2_MAC), (br3, VM13_BR3_MAC)],
        disks=[(user_data_disk13, "device=cdrom"), (disk13, "")]
    )

    # vm 14
    disk14.create_from_base_img(base_img, size=10)
    user_data14.create(
        password=PASSWORD,
        pubkey=PUB_KEY,
        nameservers=[DNS_ADDRESS]
    )
    network_config14.create(VM14_NETWORK_CONFIG)
    user_data_disk14.create_with_cloud_localds(
        user_data=user_data14,
        network_config=network_config14
    )
    vm14.install(
        bridges=[(br0, VM14_BR0_MAC), (br3, VM14_BR3_MAC)],
        disks=[(user_data_disk14, "device=cdrom"), (disk14, "")]
    )

def teardown():
    vm11.destroy()
    vm12.destroy()
    vm13.destroy()
    vm14.destroy()
    user_data_disk11.delete()
    user_data_disk12.delete()
    user_data_disk13.delete()
    user_data_disk14.delete()
    network_config11.delete()
    network_config12.delete()
    network_config13.delete()
    network_config14.delete()
    user_data11.delete()
    user_data12.delete()
    user_data13.delete()
    user_data14.delete()
    disk11.delete()
    disk12.delete()
    disk13.delete()
    disk14.delete()
    br3_direct_rule.delete()
    br3.teardown()
    br2_direct_rule.delete()
    br2.teardown()
    br1_direct_rule.delete()
    br1.teardown()
    br0_nat_rule.delete()
    br0.teardown()

def check():
    vm11.set_access_info(
        host=VM11_BR0_ADDRESS,
        pkey=PRIV_KEY,
        passphrase=PRIV_KEY_PASS,
        user="ubuntu"
    )
    vm12.set_access_info(
        host=VM12_BR0_ADDRESS,
        pkey=PRIV_KEY,
        passphrase=PRIV_KEY_PASS,
        user="ubuntu"
    )
    vm13.set_access_info(
        host=VM13_BR0_ADDRESS,
        pkey=PRIV_KEY,
        passphrase=PRIV_KEY_PASS,
        user="ubuntu"
    )
    vm14.set_access_info(
        host=VM14_BR0_ADDRESS,
        pkey=PRIV_KEY,
        passphrase=PRIV_KEY_PASS,
        user="ubuntu"
    )
    while(vm11.ping() == False or vm12.ping() == False or vm13.ping() == False or vm14.ping() == False):
        time.sleep(1)

def start():
    vm12.shell(" && ".join([
        "sudo apt update",
        "sudo apt install libc-ares2",
        "sudo wget https://github.com/FRRouting/frr/releases/download/frr-6.0/frr_6.0-1.ubuntu18.04+1_amd64.deb -O /frr.deb",
        "sudo dpkg -i /frr.deb",
        "sudo sed -i -e 's/=no/=yes/g' /etc/frr/daemons",
        "sudo /usr/lib/frr/frr restart",
        " ".join([
            'sudo vtysh -c "conf t"',
            '-c "router bgp 100"',
            '-c "bgp router-id 1.1.1.1"',
            f'-c "neighbor {VM13_BR2_ADDRESS} remote-as 200"',
            f'-c "network {BR1_SUBNET}"'
        ]),
        'sudo vtysh -c "copy running-config startup-config"',
        'sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"'
    ]))
    vm13.shell(" && ".join([
        "sudo apt update",
        "sudo apt install libc-ares2",
        "sudo wget https://github.com/FRRouting/frr/releases/download/frr-6.0/frr_6.0-1.ubuntu18.04+1_amd64.deb -O /frr.deb",
        "sudo dpkg -i /frr.deb",
        "sudo sed -i -e 's/=no/=yes/g' /etc/frr/daemons",
        "sudo /usr/lib/frr/frr restart",
        " ".join([
            'sudo vtysh -c "conf t"',
            '-c "router bgp 200"',
            '-c "bgp router-id 2.2.2.2"',
            f'-c "neighbor {VM12_BR2_ADDRESS} remote-as 100"',
            f'-c "network {BR3_SUBNET}"'
        ]),
        'sudo vtysh -c "copy running-config startup-config"',
        'sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"'
    ]))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("mode", choices=["setup", "teardown"])
    args = parser.parse_args()

    privileged_or_exit()

    if args.mode == "setup":
        try:
            setup()
            check()
            start()
            print("Successfully done")
        except Exception as e:
            print("Error detected. *** teardown ***")
            teardown()
            raise e
    elif args.mode == "teardown":
        teardown()
    else:
        print("unknown command", args.mode)

