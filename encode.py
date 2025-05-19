
def transform_byte_into_bits(byte, read_bits, bits_counter, overflow):
    overflow_counter = 0 
    for i in range(8):
        if bits_counter < 26:  
            read_bits = (read_bits << 1) | ((byte[0] >> i) & 1)
            bits_counter += 1
        else:
            overflow = (overflow << 1) | ((byte[0] >> i) & 1)
            overflow_counter += 1
    return (read_bits, overflow, bits_counter, overflow_counter)

def read_26bits(filename):
    with open(filename, 'rb') as file:
        overflow = 0
        overflow_counter = 0
        while True:
            read_bits = overflow
            bits_counter = overflow_counter

            while bits_counter < 26:
                byte = file.read(1)
                if not byte: 
                    if bits_counter > 0:  
                        yield read_bits
                    return  

                overflow = 0
                read_bits, overflow, bits_counter, overflow_counter = transform_byte_into_bits(byte, read_bits, bits_counter, overflow)
            
            yield read_bits
            
def encode(filename):
    """Encodes the given file in Hamming (31, 26).

    Args:
        filename (str): The name of the file to be encoded.
    
    Returns:
        None
    """
    for chunk in read_26bits(filename):
        print(f"{chunk:026b}")


