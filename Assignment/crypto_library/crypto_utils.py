from pseudo_random_gen import gen, singler
import time


def add_zeros_at_end(string, padding_size):
    return string[::-1].zfill(padding_size)[::-1]


def add_zeros_at_front(string, padding_size):
    return string.zfill(padding_size)


def split_text(message, block_size):
    chunks = [message[i:i+block_size]
              for i in range(0, len(message), block_size)]
    return chunks


def xor(bin_x, bin_y):
    '''
    xor of the two binary strings
    '''
    return "".join(str(ord(x) ^ ord(y)).replace('0b', '') for x, y in zip(bin_x, bin_y))


def dec_to_bin_wo_pad(x):
    """dec_to_bin converts decimal to binary

    Args:
        x (int): integer

    Returns:
        str : binary string
    """
    return bin(x).replace('0b', '')


def dec_to_bin(x, size):
    '''
    convert decimal to binary
    '''
    return bin(x).replace('0b', '').zfill(size)


def bin_to_dec(x):
    return int(x, 2)


def get_random_bits(size):
    '''
    Generate random binary string of specified bits
    '''
    now = (round(time.time() * 1000)) % (2**size)
    in_binary = dec_to_bin(now, size)
    random_identifier = gen(in_binary, singler)
    return random_identifier


def randint(low, high):
    '''
    Generate random integer between (low <= high)
    '''
    range = high-low+1
    now = (round(time.time() * 1000))
    in_bin = bin(now).replace('0b', '')
    random_val = gen(in_bin, doubler)
    in_dec = bin_to_dec(random_val)
    final = low+in_dec % range
    return final


def str_to_bin(s):
    return dec_to_bin_wo_pad(int.from_bytes(s.encode(), 'big'))


def bin_to_str(n):
    x = bin_to_dec(n)
    return x.to_bytes((x.bit_length() + 7) // 8, 'big').decode()
