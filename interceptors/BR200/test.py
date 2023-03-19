import os
import sys
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from disectors.PhotonFusion.FusionDisector import FusionRecvDisector

data = b"\x00\x00\x00\x02R\xec\xca\x13\x0b\xd0[^\x01\x00\x00\x00\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x08\x9f\x06\x00\x01\x00\x00\x00\x01\xce\x00\x00\x00\x04\xf3\x83\x84\xbd\x98\x1fH\x1c\x9b\x92\xaf\x1a\xa9<c\xda\x9b\xd0\xe8\x01\x88\xf2\xc8<F\xa0 q}6\x82\xc0\xe0$.\\\xce\x1cO.<\x03>\xb4\xd5c@.2i\x11\x13\xded\xd1\xf0\x87\xa3\xf1\xf4\x99\x08V\x85\xa4<\xbb\x115*\xb8\x8f\xa8\xa7]\xe9\x81\x11\xa6\x15\x0b\x1f\xac\xdbFe\x98zH\xf3\x10P\xab\xf2\x0e\xd8\x9b\xfb\xc0/\xf5\x07\xa9?\x83A\x01\xb3\xd1\xf8i\x1a\x8b%\xa0V\xf20\xcd\xe9\x96s\xf0\xa5\xd9\xfa\xd5\xf3h\xbf\x1a\xb4\xd4\xa4lKC\x07\x1aa\xce\x0b.\xbb\xbdk7\x1ae/\xaf\xe1\xb4F(_96W'\xafC\xef\xaf\xb3\xff\xcf\xd5K\xfb_s\x1e\x81\x8a7\xe7m\xb5\xd3\xe7\xd4\xda\xdc\n\x92\xd2\x87\xd7\xc8\xd1\xc6\x81\x80^7\x1e\x1e\x1a\xc5\xfb\x9c\xc4\x10\xfc\xb6&\x01\x864\xe1\xeb\xf0P\x83\x8d\x08\x82\x1cPh(\xe3H\xa1\xad\x83\xb0P\x84\xe4\xa57Y\n\xb9\x13p`\x8e\x04\xc9]m\x03MS\xaaug\x01\xe3\x8c\xe6\xae-R?}\x90\xba\xcf$\xb7\xa8.\x13\xb6z\xf8\xbf\xf2\xf5\xd9%\x8f\x99\x91\x96%\xfe\x1e\x14\x0e\x92\xf7Pp\xe7\xb5|\xc0\x07\xf8\xe7[\x81\x18\xf7\xcd\x9c\xb4\xd2S\xf5\x0f\x19\x8aV\x04\xa3X\x08\xe6V=\xd4\x85\xd8X\x04D\xd5\xa4{\xde\x0eI\x9d\x0cD\xa2 \x84\xc1V\xf7\xd5Yj2\xf1\tY\xfa\xaf\xadkj\xf8Y\xcb\xb3L\xec\xc8nI\x99\x94\xb8\xa3\xa9*<\x1a\x18W\x1c\xff15Q\x84\xa6\xc2\xcfQN\n\xf6\xd1\xbe%o:qsT\x03\x18\xcd\x0cB\xf1j\x99\x9a4|\x1f\xd6\xf0b0\xaa\x9d\t&VP\xb9\xf1a=\xf5\xf8\x94\xda/#\xa1\xa4]5\x0cf\x15r\xa6\xab\nkMi\xf5\xb7\xed?L\xae\x9a~NE 6\x1f\x0cv"

packet = FusionRecvDisector(data)
packet.deserialize()
print(packet.command.commandType)