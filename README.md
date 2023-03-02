# Python Proxy
Co-Made with ChatGpt

# How to use.
1. Know the ip and port of the server you are trying to connect to
2. Make that ip point to your loopback interface with `netsh int ip add address "Loopback" <ip>`, if intercepting https, just change the hostname in /etc/hosts
3. Obtain your local ip on your network interface/non loopback interface using ifconfig/ipconfig
4. Open proxy.py, and change the parameters to your local_ip, remote_ip and the port
5. For ssl connections like https, generate a cert and key first using the GENERATE.py, change the CN fields
6. Install the generated server.der to your localmachine trusted root certificates
