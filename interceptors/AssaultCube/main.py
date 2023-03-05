import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from proxy import TcpProxy, UdpProxy
from disectors.AssaultCube.ServerRetriever import ServerRetrieverDisector

def serverRetriverCallback(data, toServer):
    if(not toServer): #Check if it come from server
        try:
            serverRetrieverpacket = ServerRetrieverDisector(data) #Analyze the packet using ServerRetrieverDisector
            serverRetrieverpacket.deserialize() #call Deserialize function
            for ip, port in serverRetrieverpacket.serverList:
                print(f"{ip}:{port}")
        except:
            string = str(data)

        #print(string)
    return data

def sortpckServerCallback(data, toServer):
    try:
        string = data.decode()
    except:
        string = str(data)

    print(string)
    return data

# Proxies
serverRetriever = TcpProxy('0.0.0.0', 28760, '167.114.125.195', 28760, True, serverRetriverCallback)
serverRetriever.start()

sortpckServer = UdpProxy('0.0.0.0', 4001, '167.114.34.178', 4001, True, sortpckServerCallback)
sortpckServer.start()

while True:
    pass