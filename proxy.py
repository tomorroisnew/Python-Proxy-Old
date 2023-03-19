import socket
import threading
import socket
import ssl
import threading
from loguru import logger

def getLocalIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def logPackets(data, toServer):
    if(toServer):
        print("[client] {}".format(str(data)))
    else:
        print("[server] {}".format(str(data)))
    return data

class TcpProxy(threading.Thread):
    def __init__(self, local_host, local_port, remote_host, remote_port, useLocalIp, intercept_callback = logPackets):
        threading.Thread.__init__(self)
        self.local_host = local_host
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.intercept_callback = intercept_callback
        self.useLocalIp = useLocalIp

    def receive_from(self, client_socket, remote_socket):
        while True:
            try:
                data = remote_socket.recv(4096)
            except:
                continue
            if not data:
                continue
            # Edit the received data here
            modified_data = self.intercept_callback(data, False)  # replace this line with your own logic for editing packets
            client_socket.sendall(modified_data)
        remote_socket.close()
        client_socket.close()

    def send_to(self, client_socket, remote_socket):
        while True:
            try:
                data = client_socket.recv(4096)
            except:
                continue
            #data = client_socket.recv(4096)
            if not data:
                continue
            # Edit the received data here
            modified_data = self.intercept_callback(data, True)  # replace this line with your own logic for editing packets
            remote_socket.sendall(modified_data)
        client_socket.close()
        remote_socket.close()

    def handle_client(self, client_socket):
        # Connect to the remote server
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(self.useLocalIp):
            remote_socket.bind((getLocalIp(), 0))
        remote_socket.connect((self.remote_host, self.remote_port))

        # Create separate threads for sending and receiving data
        receive_thread = threading.Thread(target=self.receive_from, args=(client_socket, remote_socket))
        send_thread = threading.Thread(target=self.send_to, args=(client_socket, remote_socket))
        receive_thread.start()
        send_thread.start()

    def run(self):
        # Create a socket for the server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.local_host, self.local_port))
        server_socket.listen(5)
        print(f'[*] Listening on {self.local_host}:{self.local_port}')

        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print(f'[*] Accepted connection from {client_address[0]}:{client_address[1]}')

            # Handle the client in a separate thread
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

class TcpSSLProxy(threading.Thread):
    def __init__(self, local_host, local_port, remote_host, remote_port, useLocalIp, ssl_certfile=None, ssl_keyfile=None, intercept_callback = logPackets):
        threading.Thread.__init__(self)
        self.local_host = local_host
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.ssl_certfile = ssl_certfile
        self.ssl_keyfile = ssl_keyfile
        self.intercept_callback = intercept_callback
        self.useLocalIp = useLocalIp

    def receive_from(self, client_socket, remote_socket):
        while True:
            try:
                data = remote_socket.recv(65534)
            except:
                continue
            if not data:
                continue
            # Edit the received data here
            modified_data = self.intercept_callback(data, False)  # replace this line with your own logic for editing packets
            client_socket.sendall(modified_data)
        remote_socket.close()
        client_socket.close()

    def send_to(self, client_socket, remote_socket):
        while True:
            data = client_socket.recv(65534)
            if not data:
                break
            # Edit the received data here
            modified_data = self.intercept_callback(data, True)  # replace this line with your own logic for editing packets
            remote_socket.sendall(modified_data)
        client_socket.close()
        remote_socket.close()

    def handle_client(self, client_socket):
        # Connect to the remote server
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(self.useLocalIp):
            remote_socket.bind((getLocalIp(), 0))
        remote_socket.connect((self.remote_host, self.remote_port))

        # Create an SSL context for the remote socket
        context = ssl.create_default_context()
        remote_socket = context.wrap_socket(remote_socket, server_hostname='google.com')

        # Create an SSL context for the client socket
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=self.ssl_certfile, keyfile=self.ssl_keyfile)

        # Wrap the client socket with SSL encryption
        client_socket = context.wrap_socket(client_socket, server_side=True)

        # Create separate threads for sending and receiving data
        receive_thread = threading.Thread(target=self.receive_from, args=(client_socket, remote_socket))
        send_thread = threading.Thread(target=self.send_to, args=(client_socket, remote_socket))
        receive_thread.start()
        send_thread.start()

    def run(self):
        # Create a socket for the server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.local_host, self.local_port))
        server_socket.listen(5)
        print(f'[*] Listening on {self.local_host}:{self.local_port}')

        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print(f'[*] Accepted connection from {client_address[0]}:{client_address[1]}')

            # Handle the client in a separate thread
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

# My own shit code

import socket
import threading

class UdpProxy(threading.Thread):
    def __init__(self, local_host, local_port, remote_host, remote_port, useLocalIp, intercept_callback=logPackets):
        threading.Thread.__init__(self)
        self.local_host = local_host
        self.remote_host = remote_host
        self.local_port = local_port
        self.remote_port = remote_port
        self.intercept_callback = intercept_callback
        self.useLocalIp = useLocalIp
        self.client_server_map = {}
        self.client_server_map_lock = threading.Lock()

    def receive_from(self, client_address, server_socket):
        try:
            while True:
                if server_socket.fileno() == -1:  # Check if the server socket is still valid.
                    break
                data, _ = server_socket.recvfrom(65534)
                data = self.intercept_callback(data, False)
                try:
                    self.client_socket.sendto(data, client_address)
                except socket.error as e:
                    print(f"Error sending to client {client_address}: ", e)
                    break
        except socket.error as e:
            if server_socket.fileno() != -1:  # Only print the error if the server socket is still valid.
                print(f"Error receiving from server for client {client_address}: ", e)
        finally:
            server_socket.close()
            with self.client_server_map_lock:
                del self.client_server_map[client_address]

    def handle_client(self, client_address):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.useLocalIp:
            server_socket.bind((getLocalIp(), 0))

        with self.client_server_map_lock:
            self.client_server_map[client_address] = server_socket

        receive_thread = threading.Thread(target=self.receive_from, args=(client_address, server_socket))
        receive_thread.start()


    def run(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.client_socket.bind((self.local_host, self.local_port))
    
            while True:
                try:
                    data, client_address = self.client_socket.recvfrom(65534)
                except ConnectionResetError as cre:
                    print(f"Client connection {client_address} was forcibly closed by the remote host.")
                    with self.client_server_map_lock:
                        if client_address in self.client_server_map:
                            self.client_server_map[client_address].close()
                            del self.client_server_map[client_address]
                    continue
                
                if client_address not in self.client_server_map:
                    self.handle_client(client_address)
    
                data = self.intercept_callback(data, True)
                server_socket = self.client_server_map[client_address]
                server_socket.sendto(data, (self.remote_host, self.remote_port))
        except socket.error as e:
            print("Error starting proxy: ", e)
            self.client_socket.close()
            for server_socket in self.client_server_map.values():
                server_socket.close()

#import socket
#import threading
#import time
#import select
#
#class UdpProxy(threading.Thread):
#    def __init__(self, local_host, local_port, remote_host, remote_port, useLocalIp, intercept_callback=logPackets, max_attempts=3):
#        threading.Thread.__init__(self)
#        self.local_host = local_host
#        self.remote_host = remote_host
#        self.local_port = local_port
#        self.remote_port = remote_port
#        self.intercept_callback = intercept_callback
#        self.client_address = None
#        self.useLocalIp = useLocalIp
#        self.server_connected = False
#        self.max_attempts = max_attempts
#        self.receive_attempts = 0
#        self.send_attempts = 0
#
#    def wait_for_client(self):
#        self.client_socket.setblocking(True)  # set client socket to blocking mode
#
#        while True:
#            try:
#                data, self.client_address = self.client_socket.recvfrom(65534)
#                logger.debug("Client connected from:", self.client_address)
#
#                # send the first packet to the remote server
#                self.server_socket.sendto(data, (self.remote_host, self.remote_port))
#                logger.debug("Initial Data Sent to server")
#
#                break
#            except socket.error:
#                pass
#
#        self.client_socket.setblocking(False)  # set client socket back to non-blocking mode
#
#        inputs = [self.client_socket, self.server_socket]
#        outputs = []
#        logger.debug("Starting to loop through accepting and receiving")
#        while inputs:
#            try:
#                # use select to wait for data on both sockets
#                readable, writable, exceptional = select.select(inputs, outputs, inputs)
#
#                # process any data received from the client socket
#                for s in readable:
#                    if s is self.client_socket:
#                        data, address = s.recvfrom(65534)
#                        data = self.intercept_callback(data, True)
#                        # process data received from client
#                        self.server_socket.sendto(data, (self.remote_host, self.remote_port))
#                    elif s is self.server_socket:
#                        data, address = s.recvfrom(65534)
#                        data = self.intercept_callback(data, False)
#                        # process data received from server
#                        self.client_socket.sendto(data, self.client_address)
#
#                # process any data received from the server socket
#                for s in exceptional:
#                    # handle any errors that occur on the sockets
#                    pass
#
#                for s in writable:
#                    # handle any sockets that are ready for writing
#                    pass
#
#            except KeyboardInterrupt:
#                # handle keyboard interrupt
#                break
#
#        # cleanup
#        self.client_socket.close()
#        self.server_socket.close()
#
#
#
#    def receive_from(self):
#        while True:
#            try:
#                data, self.client_address = self.client_socket.recvfrom(65534)
#                data = self.intercept_callback(data, True)
#                self.server_socket.sendto(data, (self.remote_host, self.remote_port))
#                self.server_connected = True
#            except socket.error as e:
#                logger.debug("Error receiving from client: ", e)
#                self.receive_attempts += 1
#                if self.receive_attempts >= self.max_attempts:
#                    logger.debug("Max receive attempts reached. Closing sockets and ending thread...")
#                    self.client_socket.close()
#                    self.server_socket.close()
#                    return
#                else:
#                    time.sleep(1) # wait for 1 second before retrying
#
#    def send_to(self):
#        while True:
#            try:
#                data, server_address = self.server_socket.recvfrom(65534)
#                data = self.intercept_callback(data, False)
#                try:
#                    self.client_socket.sendto(data, self.client_address)
#                except socket.error as e:
#                    print("Error sending to client: ", e)
#                    self.send_attempts += 1
#                    if self.send_attempts >= self.max_attempts:
#                        print("Max send attempts reached. Closing sockets and ending thread...")
#                        self.client_socket.close()
#                        self.server_socket.close()
#                        return
#                    else:
#                        time.sleep(1) # wait for 1 second before retrying
#            except socket.error as e:
#                print("Error receiving from server: ", e)
#                self.send_attempts += 1
#                if self.send_attempts >= self.max_attempts:
#                    print("Max send attempts reached. Closing sockets and ending thread...")
#                    self.client_socket.close()
#                    self.server_socket.close()
#                    return
#                else:
#                    time.sleep(1) # wait for 1 second before retrying
#
#    def run(self):
#        try:
#            # Create sockets for the client and server
#            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#            self.server_socket.settimeout(30)
#            if(self.useLocalIp):
#                self.server_socket.bind((getLocalIp(), 0))
#
#            # Bind the client socket to the local host and port
#            self.client_socket.bind((self.local_host, self.local_port))
#
#            # Create separate threads for sending and receiving data
#            self.receive_thread = threading.Thread(target=self.receive_from)
#            #receive_thread.start()
#            self.send_thread = threading.Thread(target=self.send_to)
#
#            #send_thread.start()
#
#            # Wait for a connection from the client
#            print("Waiting for client to connect...")
#            self.wait_for_client()
#
#        except socket.error as e:
#            print("Error starting proxy: ", e)
#            self.client_socket.close()
#            self.server_socket.close()
#