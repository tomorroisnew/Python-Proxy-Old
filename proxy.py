import socket
import threading
import socket
import ssl
import threading

def logPackets(data, toServer):
    if(toServer):
        print("[client] {}".format(str(data)))
    else:
        print("[server] {}".format(str(data)))
    return data

class TcpProxy(threading.Thread):
    def __init__(self, local_host, local_port, remote_host, remote_port, intercept_callback = logPackets):
        threading.Thread.__init__(self)
        self.local_host = local_host
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.intercept_callback = intercept_callback

    def receive_from(self, client_socket, remote_socket):
        while True:
            data = remote_socket.recv(4096)
            if not data:
                break
            # Edit the received data here
            modified_data = self.intercept_callback(data, False)  # replace this line with your own logic for editing packets
            client_socket.sendall(modified_data)
        remote_socket.close()
        client_socket.close()

    def send_to(self, client_socket, remote_socket):
        while True:
            data = client_socket.recv(4096)
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
        remote_socket.bind(('192.168.18.6', 0))
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
    def __init__(self, local_host, local_port, remote_host, remote_port, ssl_certfile=None, ssl_keyfile=None, intercept_callback = logPackets):
        threading.Thread.__init__(self)
        self.local_host = local_host
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.ssl_certfile = ssl_certfile
        self.ssl_keyfile = ssl_keyfile
        self.intercept_callback = intercept_callback

    def receive_from(self, client_socket, remote_socket):
        while True:
            try:
                data = remote_socket.recv(4096)
            except:
                remote_socket.close()
                client_socket.close()
                return
            if not data:
                break
            # Edit the received data here
            modified_data = self.intercept_callback(data, False)  # replace this line with your own logic for editing packets
            client_socket.sendall(modified_data)
        remote_socket.close()
        client_socket.close()

    def send_to(self, client_socket, remote_socket):
        while True:
            data = client_socket.recv(4096)
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
        remote_socket.bind(('192.168.18.6', 0))
        remote_socket.connect((self.remote_host, self.remote_port))

        # Create an SSL context for the remote socket
        context = ssl.create_default_context()
        remote_socket = context.wrap_socket(remote_socket, server_hostname='test')

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
    def __init__(self, local_host, local_port , remote_host, remote_port, intercept_callback = logPackets):
        threading.Thread.__init__(self)
        self.local_host = local_host
        self.remote_host = remote_host
        self.local_port = local_port
        self.remote_port = remote_port
        self.intercept_callback = intercept_callback
        self.client_address = None

    def receive_from(self):
        while True:
            data, self.client_address = self.client_socket.recvfrom(4096)
            data = self.intercept_callback(data, True)
            self.server_socket.sendto(data, (self.remote_host, self.remote_port))

    def send_to(self):
        while True:
            data, server_address = self.server_socket.recvfrom(4096)
            data = self.intercept_callback(data, False)
            self.client_socket.sendto(data, self.client_address)

    def run(self):
        # Create sockets for the client and server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('192.168.18.6', 0))

        # Bind the client socket to the local host and port
        self.client_socket.bind((self.local_host, self.local_port))

        # Create separate threads for sending and receiving data
        receive_thread = threading.Thread(target=self.receive_from)
        send_thread = threading.Thread(target=self.send_to)
        receive_thread.start()
        send_thread.start()
