import os
from commonFunctions import identify_parity_bits, read_nbits

def add_chunk_to_message(chunk, message, chunk_length=26):
    """Adds a chunk of data to the message while tracking the positions of ones.
    Args:
        chunk (int): The data chunk to be added.
        message (int): The current message to which the chunk will be added.
        chunk_length (int): Number of valid bits in the chunk (for last chunk).
    Returns:
        int: The updated message and list of positions of ones.
    """
    parity_bits = identify_parity_bits(31)
    ones_in_the_chunk = []
    chunk_idx = chunk_length - 1 
    message = 0 

    for pos in range(1, 32): 
        if pos not in parity_bits:
            if chunk_idx >= 0:
                bit = (chunk >> chunk_idx) & 1
                chunk_idx -= 1
            else:
                bit = 0 
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
        xor_result ^= one & 0b11111  # Mask to 5 bits

    for counter, parity in enumerate(parity_bits):
        xor_bit = (xor_result >> counter) & 1
        position = 31 - parity

        if xor_bit == 1:
            message = (message | (1 << position))
        else:
            message = (message & ~(1 << position))

    return message


def insert_parity_bits(chunk, chunk_length=26):
    """Given a 26-bit chunk, this function inserts 5 parity bits to create a 31-bit message.
    Args:
        chunk (int): The data chunk to be processed.
    Returns:
        int: The 31-bit message with parity bits added.
    """
    message = 0
    parity = 0
    ones_in_the_chunk = []

    message, ones_in_the_chunk = add_chunk_to_message(chunk, message, chunk_length)
    parity_bits = identify_parity_bits(31)
    parity = add_parity_to_message(ones_in_the_chunk, parity_bits, message)

    return parity

def write_31bits(file, message):
    """Writes the 31-bit encoded message to a file.

    Args:
        file: The file object to write the encoded message to.
        message (int): The 31-bit encoded message to be written.
    """
    num_32bits = message & 0xFFFFFFFF
    file.write(str(num_32bits))
    file.write(" ") 

            
def encode(filename):
    """Encodes the given file in Hamming (31, 26) and writes the encoded data to a new file.
    Args:
        filename (str): The name of the file to be encoded.
    Returns:
        None
    """
    directory = "./out/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    new_filename = filename.split("/")[-1].split(".")[0] + ".hamming"
    new_filename = os.path.join(directory, new_filename)

    file = open(new_filename, 'w')
    
    for chunk, chunk_length in read_nbits(filename, 26):
        message = insert_parity_bits(chunk, chunk_length)
        write_31bits(file, message)

    file.close()



