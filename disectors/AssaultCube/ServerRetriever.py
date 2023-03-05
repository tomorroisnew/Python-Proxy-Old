from disectors.BaseDisector import Disector

class ServerRetrieverDisector(Disector):
    def __init__(self, buffer) -> None:
        super().__init__(buffer)
        self.serverList = []

    def deserialize(self):
        servers = self.buffer.readBytes(len(self.buffer.buffer)).decode()
        for line in servers.strip().split('\n'):
            if('addserver' in line):
                #print(line)
                _, ip, port = line.split()
                self.serverList.append((ip, port))