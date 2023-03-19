from disectors.BaseDisector import Disector
from disectors.BaseDisector import Buffer
from disectors.PhotonFusion.Encryption import DiffieHellmanCryptoProvider

class Protocol18:
    @staticmethod
    def Read(stream, gpType, flags = 0, parameters = None):
        if(gpType >= 128):
            num = gpType - 128
        else:
            num = gpType

        if(num >= 64):
            num2 = num - 64
        else:
            num

        flag = (flags & 2) == 2
        flag2 = (gpType >= 128) and (gpType <= 228)
        
        if(not flag2):
            if(gpType == 8):
                return None
            if(gpType == 67):
                num = Protocol18.ReadCompressedUInt32(stream)
                #print(num)
                return stream.readBytes(num)

    @staticmethod
    def ReadParameterDictionary(stream: Buffer, target = None, flags = 0):
        num = int.from_bytes(stream.readBytes(1), 'little')
        parameterDictionary = {}
        flag = (flags & 1) == 1
        for i in range(num):
            code = int.from_bytes(stream.readBytes(1), 'little')
            b = int.from_bytes(stream.readBytes(1), 'little')
            #print(b)
            flag2 = (flag and b == 67)
            if(flag2):
                pass
            else:
                value = Protocol18.Read(stream, b)
                #print(len(value))

            parameterDictionary[code] = value

        return parameterDictionary

    @staticmethod
    def ReadCompressedUInt32(buffer: Buffer):
        num = 0
        num2 = 0
        while(num2 != 35):
            b = buffer.readBytes(1)
            num |= ((((b[0] & 127)& 0xFFFFFFFF) << num2) & 0xFFFFFFFF)
            print(num)
            num2 += 7
            flag2 = (b[0] & 128) == 0
            if(flag2):
                break

        print(num)
        return num

class OperationResponse(Disector):

    def deserialize(self):
        self.OperationCode = int.from_bytes(self.buffer.readBytes(1), 'big')
        self.ReturnCode = int.from_bytes(self.buffer.readBytes(2), 'little', signed=True)
        gpType = int.from_bytes(self.buffer.readBytes(1), 'little')
        self.DebugMessage = Protocol18.Read(self.buffer, gpType)
        self.Parameters = Protocol18.ReadParameterDictionary(self.buffer)



class Payload(Disector):

    def deserialize(self):
        self.operation = int.from_bytes(self.buffer.readBytes(1), 'big')
            #print(self.operation)

        if(self.operation != (243 or 253)):
            return

        b = self.buffer.readBytes(1)
        self.messageType = b[0] & 127  #internal enum EgMessageType : byte
        self.flag = (b[0] & 128) > 0

        #print(self.messageType)
        if(self.messageType != 1):
            if(self.flag): #Encrypted
                pass
            
        if(self.messageType == 1):
            # this.InitCallback();
            pass
        elif(self.messageType == 3): # OperationResponse
            pass
        elif(self.messageType == 4): #Event
            pass
        elif(self.messageType == 7):
            #self.Payload.currentOffset = self.Payload.currentOffset + 2  #stream.Seek(2L, SeekOrigin.Begin);
            self.operationResponse = OperationResponse(self.buffer)
            self.operationResponse.deserialize()
            
            if(self.operationResponse.OperationCode == 0): #operationResponse.OperationCode == PhotonCodes.InitEncryption;
                self.DeriveSharedKey(self.operationResponse)

    def DeriveSharedKey(self, operationResponse: OperationResponse):
        flag = operationResponse.ReturnCode != 0
        if(flag):
            pass
        else:
            array = operationResponse.Parameters[1] #operationResponse.Parameters[PhotonCodes.ServerKey];
            flag2 = (array == None) or (len(array) == 0)
            if(not flag2):
                dh_provider = DiffieHellmanCryptoProvider.instance()
                dh_provider.derive_shared_key(array)


class NCommand(Disector):

    def deserialize(self):
        #internal NCommand(EnetPeer peer, byte[] inBuff, ref int readingOffset)
        self.commandType = int.from_bytes(self.buffer.readBytes(1), 'big')
        self.commandChannelID = int.from_bytes(self.buffer.readBytes(1), 'little', signed=True)
        self.commandFlags = self.buffer.readBytes(1)
        self.reservedByte = self.buffer.readBytes(1)
        self.Size = int.from_bytes(self.buffer.readBytes(4), byteorder='big')
        self.reliableSequenceNumber = int.from_bytes(self.buffer.readBytes(4), byteorder='big')

        #print(self.commandType)
        #switch (this.commandType)
        if(self.commandType == 1):
            self.ackReceivedReliableSequenceNumber = int.from_bytes(self.buffer.readBytes(4), byteorder='big')
            self.ackReceivedSentTime = int.from_bytes(self.buffer.readBytes(4), byteorder='big')
        elif(self.commandType == 3):
            self.peerID = int.from_bytes(self.buffer.readBytes(2), byteorder='big')
        elif(self.commandType == 6):
            self.Payload = Payload(self.buffer.readBytes(self.Size - 12))
            self.Payload.deserialize()
        elif(self.commandType == 7):
            self.unreliableSequenceNumber = int.from_bytes(self.buffer.readBytes(4), byteorder='big')
            self.Payload = Payload(self.buffer.readBytes(self.Size - 16))
            print("lol")
            self.Payload.deserialize()
        elif(self.commandType == 8):
            self.startSequenceNumber = int.from_bytes(self.buffer.readBytes(4), byteorder='big')
            self.fragmentCount = int.from_bytes(self.buffer.readBytes(4), byteorder='big')
            self.fragmentNumber = int.from_bytes(self.buffer.readBytes(4), byteorder='big')
            self.totalLength = int.from_bytes(self.buffer.readBytes(4), byteorder='big')
            self.fragmentOffset = int.from_bytes(self.buffer.readBytes(4), byteorder='big')
            self.Payload = Payload(self.buffer.readBytes(self.Size - 32))
            self.Payload.deserialize()

        ##DeserializeMessageAndCallback
        #if(hasattr(self, 'Payload')):
        #    self.operation = int.from_bytes(self.Payload.readBytes(1), 'big')
        #    #print(self.operation)
        #    if(self.operation != (243 or 253)):
        #        return
#
        #    b = self.Payload.readBytes(1)
        #    self.messageType = b[0] & 127  #internal enum EgMessageType : byte
        #    self.flag = (b[0] & 128) > 0
#
        #    #print(self.messageType)
#
        #    if(self.messageType != 1):
        #        if(self.flag): #Encrypted
        #            pass
#
        #    if(self.messageType == 1):
        #        # this.InitCallback();
        #        pass
        #    elif(self.messageType == 3): # OperationResponse
        #        pass
        #    elif(self.messageType == 4): #Event
        #        pass
        #    elif(self.messageType == 7):
        #        #self.Payload.currentOffset = self.Payload.currentOffset + 2  #stream.Seek(2L, SeekOrigin.Begin);
        #        self.operationResponse = OperationResponse(self.Payload.readBytes(1000000000000))
        #        self.operationResponse.deserialize()
#
        #        print(self.operationResponse.Parameters)





class FusionRecvDisector(Disector):
    def deserialize(self):
        # ReceiveIncomingCommands
        self.peerId = self.buffer.readBytes(2)
        self.b = self.buffer.readBytes(1)
        self.b2 = self.buffer.readBytes(1)
        self.serverSentTime = int.from_bytes(self.buffer.readBytes(4), 'little')
        self.num3 = int.from_bytes(self.buffer.readBytes(4), 'little')
        self.command = NCommand(self.buffer)
        self.command.deserialize()