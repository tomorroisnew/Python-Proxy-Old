import os
import sys
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from proxy import TcpProxy, UdpProxy

def log(data, toServer):
    with open('log.txt', 'a') as f:
        if(toServer):
            f.write("[client] {}".format(str(data)) + '\n')
        else:
            f.write("[server] {}".format(str(data))+ '\n')
    return data


sortpckServer = UdpProxy('127.0.0.1', 27000, '216.120.180.22', 27000, True, log)
sortpckServer.start()