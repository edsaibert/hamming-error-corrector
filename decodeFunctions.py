from commonFunctions import identify_parity_bits, read_nbits
import os

def xor_all_ones(n, chunk):
    """ Computes the XOR of the positions of all ones in the chunk, considering 1-indexed positions from the left (MSB).
    Args:
        n (int): number of bits 
        chunk (int): the data to process 
    Returns:
        int: the XOR of all positions with a 1 bit
    """
    result = 0
    for i in range(1, n):  
        bit = (chunk >> (n - i - 1)) & 1  
        if bit:
            result ^= i

    return result

def flip_bit(n, xor_result, chunk):
    """
    Flips the bit at position xor_result in the 32-bit chunk.
    Args:
        xor_result (int): The position to flip
        chunk (int): The 32-bit integer chunk.
    Returns:
        int: The chunk with the bit at xor_result flipped.
    """
    bit_pos = n - xor_result - 1 
    chunk ^= (1 << bit_pos)

    return chunk

def remove_parity_bits(chunk, parity_bits, message):
    """ Removes the parity bits from the chunk and returns the message.
        Args:
            chunk (str): The chunk of data to process.
            parity_bits (list): The list of positions of parity bits.
            message (int): The current message to which the chunk will be added.
        Returns:
            int: The updated message without parity bits.
    """
    chunk = chunk & 0x7FFFFFFF  
    
    data_bits = []
    for pos in range(1, 32):
        if pos not in parity_bits:
            bit = (chunk >> (31 - pos)) & 1
            data_bits.append(bit)

    message = 0
    for bit in data_bits:
        message = (message << 1) | bit

    return message

def decode_chunk(chunk):
    """ Decodes a chunk of data using hamming (31, 26) code.
        Args:
            chunk (int): The chunk of data to decode.
        Returns:
            str: The decoded chunk.
    """
    # Hamming (31, 26) decoding logic goes here

    parity_bits = identify_parity_bits(31)
    message = 0
    message = remove_parity_bits(chunk, parity_bits, message)

    return message

def transform_nBits_into_string(n, bits_counter, overflow, overflow_counter, read_bytes, chunk):
    combined = (overflow << n) | (chunk & ((1 << n) - 1))
    total_bits = overflow_counter + n

    result_bytes = []

    while total_bits >= 8:
        byte = (combined >> (total_bits - 8)) & 0xFF
        result_bytes.append(byte)
        total_bits -= 8

    new_overflow = combined & ((1 << total_bits) - 1)
    new_overflow_counter = total_bits

    read_bytes.extend(result_bytes)

    return read_bytes, 0, new_overflow, new_overflow_counter

def decode(filename):
    """ Decodes a binary file using hamming (31, 26) code.
        Args:
            filename (str): The name of the file to decode.
    """
    bits_counter = 0
    overflow = 0
    overflow_counter = 0

    directory = "./out/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    new_filename = filename.split("/")[-1].split(".")[0] + ".dec"
    new_filename = os.path.join(directory, new_filename)

    with open(new_filename, 'w', encoding='utf-8') as out_file:
        with open(filename, 'r') as file:
            data = file.read().strip().split()

            for num_str in data:
                read_bytes = []
                chunk_32_bits = int(num_str)

                xor_result = xor_all_ones(32, chunk_32_bits)
                if xor_result:
                    chunk_32_bits = flip_bit(32, xor_result, chunk_32_bits)

                decoded_chunk = decode_chunk(chunk_32_bits)

                read_bytes, bits_counter, overflow, overflow_counter = transform_nBits_into_string(
                    26, bits_counter, overflow, overflow_counter, read_bytes, decoded_chunk
                )

                for byte in read_bytes:
                    if byte != 0:
                        out_file.write(chr(byte)) 