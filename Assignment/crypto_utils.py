from pseudo_random_gen import *
import time


def xor(bin_x, bin_y):
    '''
    xor of the two binary strings
    '''
    return "".join(str(ord(x) ^ ord(y)).replace('0b', '') for x, y in zip(bin_x, bin_y))


def dec_to_bin(x):
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


def get_random_bits(size):
    '''
    Generate random binary string of specified bits
    '''
    now = (round(time.time() * 1000)) % (2**size)
    in_binary = dec_to_bin(now, size)
    random_identifier = gen(in_binary, singler)
    return random_identifier


def bin_to_dec(x):
    return int(x, 2)


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
