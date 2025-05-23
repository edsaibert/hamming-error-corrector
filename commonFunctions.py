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

def transform_byte_into_bits(n, byte, read_bits, bits_counter, overflow):
    """Adds the bits from a byte to the read_bits and overflow variables (if needed).
    Args:
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
        bit = (byte[0] >> (7 - i)) & 1 
        if bits_counter < n:
            read_bits = (read_bits << 1) | bit
            bits_counter += 1
        else:
            overflow = (overflow << 1) | bit
            overflow_counter += 1
    return (read_bits, overflow, bits_counter, overflow_counter)

def read_nbits(filename, n):
    """Reads N bits from a binary file.
    Args:
        filename (str): The name of the file to read from.
    Yields:
        int: The N bits read from the file as an integer.
    """
    with open(filename, 'rb') as file:
        overflow = 0
        overflow_counter = 0
        while True:
            read_bits = overflow
            bits_counter = overflow_counter

            while bits_counter < n:
                byte = file.read(1)
                if not byte:
                    if bits_counter > 0:
                        yield read_bits
                    return

                overflow = 0
                read_bits, overflow, bits_counter, overflow_counter = transform_byte_into_bits(
                    n, byte, read_bits, bits_counter, overflow
                )

            yield read_bits