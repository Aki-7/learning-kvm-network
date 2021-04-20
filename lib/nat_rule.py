import subprocess
from lib.bridge import Bridge
from lib.util import shell

POSTROUTING="POSTROUTING"
FORWARD="FORWARD"
INPUT="INPUT"
OUTPUT="OUTPUT"

class NatRule:
    def __init__(self, br: Bridge):
        self.br = br
        BR = br.name.upper()
        self.POST_ROUTING_CHAIN = f"MY_NAT_BRIDGE_{BR}_PRT"
        self.FORWARD_CHAIN = f"MY_NAT_BRIDGE_{BR}_FW"
        self.INPUT_CHAIN = f"MY_NAT_BRIDGE_{BR}_INP"
        self.OUTPUT_CHAIN = f"MY_NAT_BRIDGE_{BR}_OUT"
   
    def create(self, subnet: str):
        """
        subnet is like "192.168.1.0/24"
        """
        self.__create_chain(self.POST_ROUTING_CHAIN, POSTROUTING, "nat")
        self.__add_nat_rules(self.POST_ROUTING_CHAIN, subnet)
        self.__create_chain(self.FORWARD_CHAIN, FORWARD)
        self.__add_forward_rules(self.FORWARD_CHAIN, subnet)
        self.__create_chain(self.INPUT_CHAIN, INPUT)
        self.__add_input_rules(self.INPUT_CHAIN)
        self.__create_chain(self.OUTPUT_CHAIN, OUTPUT)
        self.__add_output_rules(self.OUTPUT_CHAIN)

    def delete(self):
        self.__delete_chain(self.POST_ROUTING_CHAIN, POSTROUTING, "nat")
        self.__delete_chain(self.FORWARD_CHAIN, FORWARD)
        self.__delete_chain(self.INPUT_CHAIN, INPUT)
        self.__delete_chain(self.OUTPUT_CHAIN, OUTPUT)
    
    def __create_chain(self, chain: str, parent: str, table: str = "filter"):
        shell(f"sudo iptables -t {table} -N {chain}")
        shell(f"sudo iptables -t {table} -A {parent} -j {chain}")
    
    def __delete_chain(self, chain: str, parent: str, table: str = "filter"):
        shell(f"sudo iptables -t {table} -F {chain}")
        shell(f"sudo iptables -t {table} -D {parent} -j {chain}")
        shell(f"sudo iptables -t {table} -X {chain}")

    def __add_nat_rules(self, chain: str, subnet: str):
        BASE = "sudo iptables -t nat"
        MASQUERADE = "MASQUERADE --to-ports 1024-65535"

        shell(f"{BASE} -A {chain} -s {subnet} -d 224.0.0.0/24 -j RETURN")
        shell(f"{BASE} -A {chain} -s {subnet} -d 255.255.255.255/32 -j RETURN")
        shell(f"{BASE} -A {chain} -s {subnet} ! -d {subnet} -p tcp -j {MASQUERADE}")
        shell(f"{BASE} -A {chain} -s {subnet} ! -d {subnet} -p udp -j {MASQUERADE}")
        shell(f"{BASE} -A {chain} -s {subnet} ! -d {subnet} -j MASQUERADE")
    
    def __add_forward_rules(self, chain: str, subnet: str):
        BASE = "sudo iptables"
        br_name = self.br.name
        ESTABLISHED = "-m conntrack --ctstate RELATED,ESTABLISHED"
        ICMP_UNREACHABLE_REJECT = "REJECT --reject-with icmp-port-unreachable"

        shell(f"{BASE} -A {chain} -i {br_name} -o {br_name} -j ACCEPT") # FW cross
        shell(f"{BASE} -A {chain} -d {subnet} -o {br_name} {ESTABLISHED} -j ACCEPT") # FW in
        shell(f"{BASE} -A {chain} -o {br_name} -j {ICMP_UNREACHABLE_REJECT}") # FW in
        shell(f"{BASE} -A {chain} -s {subnet} -i {br_name} -j ACCEPT") # FW out
        shell(f"{BASE} -A {chain} -i {br_name} -j {ICMP_UNREACHABLE_REJECT}") # FW out
    
    def __add_input_rules(self, chain: str):
        BASE = "sudo iptables"
        br_name = self.br.name

        shell(f"{BASE} -A {chain} -i {br_name} -p udp -m udp --dport 53 -j ACCEPT")
        shell(f"{BASE} -A {chain} -i {br_name} -p tcp -m tcp --dport 53 -j ACCEPT")
        shell(f"{BASE} -A {chain} -i {br_name} -p udp -m udp --dport 67 -j ACCEPT")
        shell(f"{BASE} -A {chain} -i {br_name} -p tcp -m tcp --dport 67 -j ACCEPT")

    
    def __add_output_rules(self, chain: str):
        BASE = "sudo iptables"
        br_name = self.br.name

        shell(f"{BASE} -A {chain} -o {br_name} -p udp -m udp --dport 53 -j ACCEPT")
        shell(f"{BASE} -A {chain} -o {br_name} -p tcp -m tcp --dport 53 -j ACCEPT")
        shell(f"{BASE} -A {chain} -o {br_name} -p udp -m udp --dport 68 -j ACCEPT")
        shell(f"{BASE} -A {chain} -o {br_name} -p tcp -m tcp --dport 68 -j ACCEPT")
    