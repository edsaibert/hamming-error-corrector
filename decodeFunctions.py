from commonFunctions import identify_parity_bits, read_nbits
import os

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
            chunk (str): The chunk of data to decode.
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

    return read_bytes, 0, new_overflow, new_overflow_counter, read_bytes

def decode(filename):
    """ Decodes a binary file using hamming (31, 26) code.
        Args:
            filename (str): The name of the file to decode.
    """
    bits_counter = 0
    overflow = 0
    overflow_counter = 0
    read_bytes = []

    with open(filename, 'r') as file:
        data = file.read().strip().split()
        for num_str in data:
            chunk_31_bits = int(num_str)
            decoded_chunk = decode_chunk(chunk_31_bits)
            print(f"Decoded chunk: {decoded_chunk:026b}")

            read_bytes, bits_counter, overflow, overflow_counter, read_bytes = transform_nBits_into_string(
                26, bits_counter, overflow, overflow_counter, read_bytes, decoded_chunk
            )

    directory = "./out/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    new_filename = filename.split("/")[-1].split(".")[0] + ".decoded"
    new_filename = os.path.join(directory, new_filename)
    with open(new_filename, 'w') as out_file:
        out_file.write(''.join(chr(byte) for byte in read_bytes))
