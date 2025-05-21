import math

def transform_byte_into_bits(byte, read_bits, bits_counter, overflow):
    """Adds the bits from a byte to the read_bits and overflow variables (if needed).
    Ags:
        byte (byte): The byte to be transformed into bits.
        read_bits (int): The bits read so far.
        bits_counter (int): The number of bits read so far.
        overflow (int): The overflow bits.
    Returns:
        read_bits (int): The updated read_bits.
        overflow (int): The updated overflow.
        bits_counter (int): The updated bits_counter.
        overflow_counter (int): The updated overflow_counter.
    """
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
    """Reads 26 bits from a binary file.
    Args:
        filename (str): The name of the file to read from.
    Yields:
        int: The 26 bits read from the file as an integer.
    """
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
    """Identifies the positions of parity bits for a given number.
    Args:
        n (int): The number for which parity bit positions are identified.
    Returns:
        list: A list of positions of parity bits.
    """
    parity_bits = [1]
    
    i = 2
    while i <= n:
        parity_bits.append(i)
        i = i * 2; 
    return parity_bits


def add_chunk_to_message(chunk, message):
    """Adds a chunk of data to the message while tracking the positions of ones.
    Args:
        chunk (int): The data chunk to be added.
        message (int): The current message to which the chunk will be added.
    Returns:
        int: The updated message and list of positions of ones.
    """
    parity_bits = identify_parity_bits(31)
    ones_in_the_chunk = []
    chunk_idx = 25  
    message = 0 
    
    for pos in range(1, 32): 
        if pos not in parity_bits:
            bit = (chunk >> chunk_idx) & 1
            chunk_idx -= 1
            message = (message << 1) | bit
            if bit == 1:
                ones_in_the_chunk.append(pos)
        else:
            message = (message << 1) | 0 
    
    return message, ones_in_the_chunk

def add_parity_to_message(ones_in_the_chunk, parity_bits, message):
    """This function does the XOR between the ones inside the data chunk and add the result as parity bits to the message.    
    Args:
        ones_in_the_chunk (list): The list of positions of ones in the chunk.
        parity_bits (list): The list of parity bit positions.
        message (int): The current message to which the parity bits will be added.
    Returns:
        int: The updated message with parity bits added.
    """
    xor_result = 0
    for one in ones_in_the_chunk:
        xor_result ^= one

    for parity in parity_bits:
        xor_bit = (xor_result >> (parity - 1)) & 1
        position = 31 - parity 

        if xor_bit == 1:
            message = (message | (1 << position))
        else:
            message = (message & ~(1 << position))
        
        
    return message


def insert_parity_bits(chunk):
    """Given a 26-bit chunk, this function inserts 5 parity bits to create a 31-bit message.
    Args:
        chunk (int): The data chunk to be processed.
    Returns:
        int: The 31-bit message with parity bits added.
    """
    message = 0
    parity = 0
    ones_in_the_chunk = []

    message, ones_in_the_chunk = add_chunk_to_message(chunk, message)
    parity_bits = identify_parity_bits(31)
    parity = add_parity_to_message(ones_in_the_chunk, parity_bits, message)

    print(f"message: {message:031b}")
    print(f"parity: {parity:031b}")
    print("")

    return parity


def encode(filename):
    """Encodes the given file in Hamming (31, 26).
    Args:
        filename (str): The name of the file to be encoded.
    Returns:
        None
    """
    for chunk in read_26bits(filename):
        print(f"chunk: {chunk:026b}")
        message = insert_parity_bits(chunk)


