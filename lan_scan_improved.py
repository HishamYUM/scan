import scapy.layers.l2
import uuid 

import csv
import logging
from prettytable import PrettyTable
import psutil
import netifaces as ni
import nmap
def select_iface():
    count = 1
    print ("[+] Available Local Networks.. ")
    interface_list = []

    for intIf in psutil.net_if_addrs().keys() :
        print (f"\t{count}) {intIf}")
        interface_list.append(intIf)
        count += 1

    choice = int(input("[+] Enter Network Number: "))
    interface_scan = interface_list[choice - 1]
    print ("[+] Network Selected: ", interface_scan)
    return  interface_list , interface_scan

def scan(interface_scan):
    ip = interface_scan.split("/")[0]
    mask = interface_scan.split("/")[1]

    
    network_scan = ip + "/" + str(mask)
    ans, unans = scapy.layers.l2.arping(network_scan, timeout=5, verbose=False)
    
    ans_list = []
    nm = nmap.PortScanner()
    
    j = 1
    for s, r in ans.res :
        host = "Host " + str(j)
        j += 1
        ipi = r.sprintf("%ARP.psrc%")
        mac = r.sprintf("%Ether.src%")
        uid = "0x" + mac.replace(":", "")
        uid = int(uid, 16)
        
        scan_ports = nm.scan(ipi, arguments='-u -Pn')
        
        try:
            open_ports = scan_ports['scan'][ipi]['tcp'].keys()
        except:
            open_ports = ["-"]
        
        try:
            machine = nm.scan(ipi, str(list(open_ports)[0]), arguments='-O -Pn')
            op_sys = machine['scan'][ipi]['osmatch'][0]['name']#[0]['osfamily']
            
        except:
            op_sys = "Unknown"
        open_ports = [str(x) for x in list(open_ports)]
        ans_list.append ([host, uuid.uuid1(uid), mac, ipi, ", ".join((open_ports)), op_sys])
        
    logging.info(ans_list)

    x = PrettyTable()
    with open('scan.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Host", "UUID", "IP", "MAC", "active TCP/UDP Ports", "OS"])
        writer.writerows(ans_list)
    x.field_names = ["Username", "UUID", "IP", "MAC", "active TCP/UDP Ports", "OS"]
    i = 1
    for hs, uud, mac, ip, open_ports, op_sys in ans_list:
        x.add_row([hs, uud, ip, mac, open_ports, op_sys])
        i += 1
    return (interface_scan, x)
network = input("Enter The Network You Want To Scan With The Mask (i.e. 192.168.56.0/24):").strip()
print(scan(network)[1])
