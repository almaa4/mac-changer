#!usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its mac address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Type new MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface , use --help for more info ")
    if not options.new_mac:
        parser.error("[-] Please specify new mac address , use --help for more info ")
    return options

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def current_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # ifconfig_result = ifconfig_result.decode('utf-8')

    mac_address_result_output = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_result_output:
        return mac_address_result_output.group(0)
    else:
        print("[-] could not read MAC address.")



options = get_arguments()

current_mac = current_mac_address(options.interface)
print(f"current MAC address : {str(current_mac)}")

change_mac(options.interface,options.new_mac)

current_mac = current_mac_address(options.interface)
if(current_mac == options.new_mac):
    print(f"[+] MAC address was successfully changed to {current_mac}")
else:
    print("[-] MAC address did not changed ")
