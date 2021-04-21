from lib.bridge import Bridge
from lib.util import shell

FORWARD="FORWARD"
INPUT="INPUT"
OUTPUT="OUTPUT"

class DirectRule:
    def __init__(self, br: Bridge):
        self.br = br
        BR = br.name.upper()
        self.FORWARD_CHAIN = f"MY_DIRECT_BRIDGE_{BR}_FWD"
        self.INPUT_CHAIN = f"MY_DIRECT_BRIDGE_{BR}_INP"
        self.OUTPUT_CHAIN = f"MY_DIRECT_BRIDGE_{BR}_OUT"

    def create(self):
        self.__create_chain(self.FORWARD_CHAIN, FORWARD)
        self.__add_direct_forward_rules(self.FORWARD_CHAIN)
        self.__create_chain(self.INPUT_CHAIN, INPUT)
        self.__add_no_input_rules(self.INPUT_CHAIN)
        self.__create_chain(self.OUTPUT_CHAIN, OUTPUT)
        self.__add_no_output_rules(self.OUTPUT_CHAIN)
        return self

    def delete(self):
        self.__delete_chain(self.FORWARD_CHAIN, FORWARD)
        self.__delete_chain(self.INPUT_CHAIN, INPUT)
        self.__delete_chain(self.OUTPUT_CHAIN, OUTPUT)
        return self
    
    def __create_chain(self, chain: str, parent: str, table: str = "filter"):
        shell(f"sudo iptables -t {table} -N {chain}")
        shell(f"sudo iptables -t {table} -A {parent} -j {chain}")

    def __delete_chain(self, chain: str, parent: str, table: str = "filter"):
        shell(f"sudo iptables -t {table} -F {chain}")
        shell(f"sudo iptables -t {table} -D {parent} -j {chain}")
        shell(f"sudo iptables -t {table} -X {chain}")
    
    def __add_direct_forward_rules(self, chain: str):
        BASE = "sudo iptables"
        br_name = self.br.name
        ICMP_UNREACHABLE_REJECT = "REJECT --reject-with icmp-port-unreachable"

        shell(f"{BASE} -A {chain} -i {br_name} -o {br_name} -j ACCEPT")
        shell(f"{BASE} -A {chain} -o {br_name} -j {ICMP_UNREACHABLE_REJECT}")
        shell(f"{BASE} -A {chain} -i {br_name} -j {ICMP_UNREACHABLE_REJECT}")
    
    def __add_no_input_rules(self, chain: str):
        BASE = "sudo iptables"
        br_name = self.br.name
        ICMP_UNREACHABLE_REJECT = "REJECT --reject-with icmp-port-unreachable"

        shell(f"{BASE} -A {chain} -i {br_name} -j {ICMP_UNREACHABLE_REJECT}")
 
    def __add_no_output_rules(self, chain: str):
        BASE = "sudo iptables"
        br_name = self.br.name
        ICMP_UNREACHABLE_REJECT = "REJECT --reject-with icmp-port-unreachable"

        shell(f"{BASE} -A {chain} -o {br_name} -j {ICMP_UNREACHABLE_REJECT}")
