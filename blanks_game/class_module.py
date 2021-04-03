from bitarray import bitarray
from .func_module import dec_to_bin


class Ip4object (object):
    """
    Definition of a 32 bit length IPv4 address, 
    and bunch of methods.
    """

    def __init__(self, address):
        self.address = dec_to_bin(address)
        print(self.address)
        # bitarray()
