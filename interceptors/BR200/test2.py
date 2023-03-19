import re
import ast

import os
import sys
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from disectors.PhotonFusion.FusionDisector import FusionRecvDisector

def intercept(data, toServer):
    if(not toServer):
        packet = FusionRecvDisector(data)
        packet.deserialize()

with open('interceptors\\BR200\\log.txt', 'r') as f:
    for line in f:
        match = re.match(r"\[(client|server)\]\s+(.*)", line)
        if match:
            group1 = match.group(1)
            group2 = group2 = match.group(2)
            data = ast.literal_eval(group2)
            if(group1 == "client"):
                toServer = True
            elif(group1 == "server"):
                toServer = False
            intercept(data, toServer)
            #print(group2)
            #bytes_data = bytes(group2)
            #print(bytes_data)
