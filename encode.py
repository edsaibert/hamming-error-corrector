
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
            

def identify_parity_bits(n):
    parity_bits = [1]
    i = 2
    while i <= n:
        parity_bits.append(i)
        i = i * 2; 
    return parity_bits


def add_chunk_to_message(chunk, message):
    parity_bits = identify_parity_bits(31)
    ones_in_the_chunk = []
    
    for i in range(31):
        if (i + 1) not in parity_bits:
            bit = (chunk >> i) & 1
            message = (message << 1) | bit
            if bit == 1:
                ones_in_the_chunk.append(i)

    return message, ones_in_the_chunk


def add_parity_to_message(ones_in_the_chunk, parity_bits, message):
    xor_result = 0
    for one in ones_in_the_chunk:
        xor_result ^= one

    for parity in reversed(parity_bits): 
        message = (message << 1) | ((xor_result >> (parity - 1)) & 1)
        
    return message


def insert_parity_bits(chunk):
    message = 0
    parity = 0
    ones_in_the_chunk = []

    message, ones_in_the_chunk = add_chunk_to_message(chunk, message)
    parity_bits = identify_parity_bits(31)
    parity = add_parity_to_message(ones_in_the_chunk, parity_bits, message)

    print("")
    print(f"message: {message:031b}")
    print(f"parity: {parity:031b}")
    print("")


def encode(filename):
    """Encodes the given file in Hamming (31, 26).

    Args:
        filename (str): The name of the file to be encoded.
    
    Returns:
        None
    """
    for chunk in read_26bits(filename):
        insert_parity_bits(chunk)


