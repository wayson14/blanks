class IpcastExceptions (BaseException):
    def __init__(self, message):
        super().__init__(self)
        self.message = message
        

class IPv4FormatError (IpcastExceptions):
    """ERROR: Data not provided in apropiate format. Correct form:
xxx.xxx.xxx.xxx (where xxx is an integer 0-255).
    """
    def __init__(self, message):
        super().__init__(self)
        self.message = message
 
class IPv4DataTypeError (IpcastExceptions):
    """ERROR: Wrong data type! Supported data types:
str, list of ints, byte/bitarray.
    """
    def __init__(self, message):
        super().__init__(self)
        self.message = message
        
 