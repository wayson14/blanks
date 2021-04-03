from bitarray import bitarray
from .exception_module import * 

def dec_to_bin(decimal):
    """
    Converts positive decimal integer into
    its binary form.
    """
    if (type(decimal)!='int'):
        decimal = int(decimal)
    if decimal == 0:
        return '0'
    bin = ''

    while(decimal > 1):
        if decimal % 2 == 0:
            bin += '0'
        else:
            bin += '1'
            decimal -= 1

        decimal /= 2
    bin += '1'
    bin = bin[::-1]  # bit string reversion

    return bin

def dec_str_to_bin_str(dec_str):
    """
    Accepts string containing 4 decimal numbers in range 0-255 divided by a dot '.'. 
    Turns them into binary representation of an IPv4 address (or mask) stored in a string object.

    """

    octet_list = []
    buffer = ''
    bin_str = ''

    if dec_str[-1] != '.':
        dec_str += '.'

    for c in dec_str:
        if c != '.':
            buffer += c
        else:
            octet_list.append(buffer)
            buffer = ''
    
    for octet in octet_list:
        l = len(dec_to_bin(octet))
        if l < 8:
            for i in range(8-l):
                bin_str += '0'
        bin_str += dec_to_bin(octet)
    
    return bin_str
        
def dec_str_to_bytearray(dec_str):
    
    octet_list = []
    buffer = ''
    bin_str = ''
    address_arr = bytearray(0)

    if dec_str[-1] != '.':
        dec_str += '.'

    for c in dec_str:
        if c != '.':
            buffer += c
        else:
            octet_list.append(buffer)
            buffer = ''
        
    for octet in octet_list:
        address_arr += bytearray([int(octet)])

    return address_arr

def address_conversion(source, dest_type = 'bytearray', address_type = 'ipv4'):
    
    """
    Converts given representation of an IP address or mask into another 
    data type, i.e. str -> bytearray
    Valid data types:
    - str
    - list (list of ints)
    - bytearray
    - bitarray
    """
    if address_type == 'ipv4':
        return ipv4_address_conversion(source, dest_type)

    elif address_type == 'ipv6':
        print("Not developed yet!")
        return ipv6_address_conversion(source, dest_type)
        
    elif address_type == 'mac':
        print("Not developed yet!")
        return mac_address_conversion(source, dest_type)

    else:
        return "Wrong address_type value!"


def ipv4_address_conversion(source, dest_type):

    outcome = 'not declared yet' #contains final product of conversion
    octet_list = [] 
    buffer = ''
    intermediary = bytearray(0) #address in intermediary form of bytes
    
    try: #checking if type of this address is valid
        source_type = type(source)
        if source_type not in (str,list,bytearray,bitarray):
            raise IPv4DataTypeError

    except IPv4DataTypeError as err:
        print(err.__doc__)
        return

    except IPv4FormatError as err:
        print(err.__doc__)
        return  


    #source to intermediary bytearray form:

    if (source_type == str): #parsing string source into bytearray format
        for c in source:
            if c.isdigit(): 
                buffer += c
            else:
                octet_list.append(buffer) 
                #print(buffer)
                buffer = ''
        else:
            octet_list.append(buffer)

        
        for octet in octet_list:
            print(octet, int(octet),bytearray([int(octet)])) 
            intermediary += (bytes([int(octet)])) 
    
    if source_type == list:
        try:
            for elem in source:
                if type(elem) is not int or elem>255 or elem < 0:
                    raise IPv4DataTypeError(f"List element: {elem} is not an 8-bit integer!")
        
        except IPv4DataTypeError as err:
            print(err.message) 
            return
        
        pass 

    if source_type == bytearray:
        pass

    if source_type == bitarray:
        pass

    #intermediary bytearray form to dest_type type outcome

    if dest_type == str:
        pass
    
    if dest_type == list:
        pass

    if dest_type == bitarray:
        pass
 
    if dest_type == bytearray:
        pass

    

    
        return outcome
        


    

   
 

###    TEST AREA

def example():   
    print("example function has worked out")

#print(dec_str_to_bytearray("255.111.6.1"),len(dec_str_to_bin_str("1.1.1.1")))

#valid string test
#print(address_conversion('192.168.1.0'))  

#int test       
#print(address_conversion(3)) 

#list test      
print(address_conversion([3,5,'g'])) 