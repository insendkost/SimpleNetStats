import os
import time
import psutil
import socket
from prettytable import PrettyTable
from prettytable import DOUBLE_BORDER

# Units of memory 

size = ['bytes', 'KB', 'MB', 'GB', 'TB']

#Get Machine IP

def get_interfaces():
    interfaces = psutil.net_if_addrs()
    active_interfaces = {}
    
    for interface_name, interface_addresses in interfaces.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET:
                active_interfaces[interface_name] = address.address
            elif address.family == socket.AF_INET6:
                pass
    return active_interfaces          

def print_network_interfaces():
    active_interfaces = get_interfaces()
    for interface, ip_address in active_interfaces.items():
        print(f"{interface}:{ip_address}")
    

def getIpAddress():
    
    interfaces = psutil.net_if_addrs()
    #Find suitable interface 
    
    for interface, addresses in interfaces.items():
        for addr in addresses:
            if addr.family == socket.AF_INET:
                return addr.address
    #IF NOTHING SUITABLE WAS FOUND
    return "N\A"



#Get Readable

def getSizes(bytes):
    for item in size:
        if bytes < 1024:
            return f"{bytes:.1f}{item}"
        bytes /= 1024
#Data Output

def printTable():
    #Main Table
    card = PrettyTable()
    card.set_style(DOUBLE_BORDER)
    
    # Names
    card.field_names = ["Total Received", "Receiving", "Total Sent", "Sending", "IP"]
    
    ip_address = getIpAddress()
    
    #Add row
    
    card.add_row([f"{getSizes(netStats2.bytes_recv)}",\
        f"{getSizes(downloadStats)}/s", 
        f"{getSizes(netStats2.bytes_sent)}",\
        f"{getSizes(uploadStats)}/s", ip_address])
    print(card)
    
    
#psutil.net_io_counters() returns network IO statistics as a named tuple
netStats1 = psutil.net_io_counters()

dataSent = netStats1.bytes_sent
dataRecv = netStats1.bytes_recv

#Running loop to get data continiously


while True:
    time.sleep(1)
    # clear is for Linux , on Windows use 'cls'
    os.system('cls')
    
    netStats2 = psutil.net_io_counters()
    
    #Rceiving/Downloading Speed
    downloadStats = netStats2.bytes_recv - dataRecv
    
    #Uploading/Sending Speed
    uploadStats = netStats2.bytes_sent - dataSent
    
    printTable()
    print_network_interfaces()
    dataSent = netStats2.bytes_sent
    dataRecv = netStats2.bytes_recv
    time.sleep(5)
    