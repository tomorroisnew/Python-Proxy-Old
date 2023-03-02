from proxy import UdpProxy

proxy = UdpProxy('0.0.0.0', 8080, '192.168.18.218', 8080)
proxy.start_server()
