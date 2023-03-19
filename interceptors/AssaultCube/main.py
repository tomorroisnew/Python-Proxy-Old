import os
import sys
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from proxy import TcpProxy, UdpProxy
from disectors.AssaultCube.ServerRetriever import ServerRetrieverDisector

def UdpCallback(data, toServer):
    print("worked")
    return data

serverList = [] # (ip, port) pairs
spawned = []

def trySpawn():
    for server in serverList:
        if(server not in spawned):
            port = int(server[1])
            ip = server[0]
            try:
                subprocess.run(['netsh', 'int', 'ip', 'add', 'address', 'loopback', ip, '255.255.255.255'], check=False, stdout=null, stderr=null)
            except:
                pass
            try:
                UdpProxy(ip, port, ip, port, True, worked).start() # The Game Listeners
            except:
                pass
            #UdpProxy('0.0.0.0', port, ip, port, False, worked).start() # ICMP Listeners
            print(f"Spawned listener: {ip}:{port}")
            spawned.append(server)

def serverRetriverCallback(data, toServer):
    if(not toServer): #Check if it come from server
        try:
            serverRetrieverpacket = ServerRetrieverDisector(data) #Analyze the packet using ServerRetrieverDisector
            serverRetrieverpacket.deserialize() #call Deserialize function
            for ip, port in serverRetrieverpacket.serverList:
                if((ip,port) not in serverList):
                    serverList.append((ip,port))
                    trySpawn()
        except:
            string = str(data)

        #print(string)
    return data

def sortpckServerCallback(data, toServer):
    try:
        string = data.decode()
    except:
        string = str(data)

    #print(string)
    return data

# Proxies
serverRetriever = TcpProxy('167.114.125.195', 28760, '167.114.125.195', 28760, True, serverRetriverCallback)
serverRetriever.start()

sortpckServer = UdpProxy('167.114.34.178', 4001, '167.114.34.178', 4001, True, sortpckServerCallback)
sortpckServer.start()

UdpProxy('167.114.34.178', 5001, '167.114.34.178', 5001, True, sortpckServerCallback).start()

UdpProxy('127.0.0.1', 9999, '54.36.188.74', 9999, True, sortpckServerCallback).start()

while True:
    pass