from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

class DiffieHellmanCryptoProvider:
    _instance = None

    def __init__(self):
        self.parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
        self.private_key = self.parameters.generate_private_key()
        self.public_key = self.private_key.public_key()

        self.shared_key = None
        self.crypto = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def derive_shared_key(self, other_party_public_key_bytes):
        pass

    def photon_big_int_array_to_ms_big_int_array(array: bytes) -> bytes:
        array = bytearray(array[::-1])  # Reverse the array
        if (array[-1] & 128) == 128:  # Check if the most significant bit is set
            array.append(0)  # Add an extra byte with value 0 at the end
        return bytes(array)

    def ms_big_int_array_to_photon_big_int_array(array: bytes) -> bytes:
        array = bytearray(array[::-1])  # Reverse the array
        if array[0] == 0:  # Check if the first byte is 0
            array = array[1:]  # Remove the first byte
        return bytes(array)
