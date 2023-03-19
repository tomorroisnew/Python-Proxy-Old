class Buffer:
    def __init__(self, buffer) -> None:
        self.buffer = bytearray(buffer)
        self.currentOffset = 0

    def readBytes(self, bytes: int):
        data = self.buffer[self.currentOffset: self.currentOffset + bytes]
        self.currentOffset += bytes
        return data

class Disector:
    def __init__(self, buffer) -> None:
        #print(type(buffer))
        if(type(buffer) != Buffer):
            self.buffer = Buffer(buffer)
        else:
            self.buffer=buffer

    def deserialize(self):
        raise NotImplemented

    def serialize(self):
        raise NotImplemented

class Test(Disector):
    def deserialize(self):
        print(self.buffer.readBytes(1))
        print(self.buffer.readBytes(1))
        print(self.buffer.readBytes(1))
        print(self.buffer.readBytes(1))
        print(self.buffer.readBytes(1))
