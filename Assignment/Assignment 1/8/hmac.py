from random import randint, getrandbits
import math


def bin_to_dec(x):
    '''
    converts binary to decimal
    '''
    return int(x, 2)


def dec_to_bin(x, size):
    '''
    Converts decimal to binary with padding
    '''
    return bin(x).replace('0b', '').zfill(size)


def dec_to_bin_wo_pad(x):
    '''
    Converts decimal to binary without padding
    '''
    return bin(x).replace('0b', '')


def generator(p, q):
    """Returns a primitive root of p

    Args:
        p (int): safe prime number
        q (int): safe prime number

    Returns:
        int: primitive root
    """
    while True:
        g = randint(2, p-1)
        if pow(g, q, p) == 1 or pow(g, 2, p) == 1:
            continue
        else:
            break
    return g


def get_group_parameters():
    """Gets the group parameters
    Working:
    For now prime no. selection is static, will move towards safe prime generation in next update with more time
    Returns:
        p,q,g,h: Returns all the group parameters
    """
    # chosen sophie germain prime
    p = 65543
    q = (p-1)//2
    g = generator(p, q)
    h = randint(0, q-1)
    while h == g:
        h = randint(0, q-1)
    return p, q, g, h


def hash(x1, x2):
    """Generates fixed length hash using DLP

    Args:
        x1 (int): input to be compressed
        x2 (int): input to be compressed

    Returns:
        int : integer after 50% compression 
    """
    return (pow(g, x1, p)*pow(h, x2, p)) % p


def hash_wrapper(x1, x2):
    """hash wrapper for binary strings
    Args:
        x1 (binary string): binary number
        x2 (binary string): binary number
    Returns:
        binary string: binary number
    """
    x1_dec = bin_to_dec(x1)
    x2_dec = bin_to_dec(x2)
    return dec_to_bin(hash(x1_dec, x2_dec), max(len(x1), len(x2)))


def split_text(message, block_size):
    """breaks the message into blocks using block size
    """
    chunks = [message[i:i+block_size]
              for i in range(0, len(message), block_size)]
    return chunks


def add_zeros_at_end(string, padding_size):
    """pad zeros at the end"""
    return string[::-1].zfill(padding_size)[::-1]


def merkle_damgard(iv, message):
    """Merkle Damgard Transform
    Working:
        Message length = L len(iv)=l
        Makes message a multiple of length l and appends message size
        iterates and applies Fixed length hashing using x2 as message and x1 as hash of previous iter
    Args:
        iv (binary string nbit): initialization vector
        message (binary string): message in binary

    Returns:
        binary string nbit: Hashed value
    """
    SIZE = len(iv)
    encoded_size = dec_to_bin(len(message), SIZE)
    messages = split_text(message, SIZE)
    messages[-1] = add_zeros_at_end(messages[-1], SIZE)
    messages.append(encoded_size)
    x1 = iv
    for m in messages:
        x2 = m
        x1 = hash_wrapper(x1, x2)
    return x1


def str_to_bin(s):
    '''
    Converts string to binary string
    '''
    return dec_to_bin_wo_pad(int.from_bytes(s.encode(), 'big'))


def xor(bin_x, bin_y):
    '''
    xor of the two binary strings
    '''
    return "".join(str(ord(x) ^ ord(y)).replace('0b', '') for x, y in zip(bin_x, bin_y))


def repeat_string(inp, length):
    '''
    Creates repeating sequences of input string of size length
    '''
    l = len(inp)
    mult = math.ceil(length/l)
    return mult*inp


def hmac(k, iv, message):
    """Calculates tag for HMAC
    Working:
        calculates xor of ipad and opad with key and performs hash with iv for first and semi last stage
        In between uses merkle damgard to calculate hash of the entire message using the ipad hash as input

    Args:
        k (binary string n bits): key for hmac
        iv (binary string n bits): Initialization vector
        message (binary string): message whose tag will be calculated

    Returns:
        binary string (n bit): Tag returned
    """
    SIZE = len(iv)
    ipad = dec_to_bin_wo_pad(0x34)
    opad = dec_to_bin_wo_pad(0x5C)
    ipad_repeat = repeat_string(ipad, len(k))
    opad_repeat = repeat_string(opad, len(k))
    xored_ipad = xor(k, ipad_repeat)
    xored_opad = xor(k, opad_repeat)
    hash_init = hash_wrapper(iv, xored_ipad)
    hash_pre_final = hash_wrapper(iv, xored_opad)
    hash_val = merkle_damgard(hash_init, message)
    final_hash = hash_wrapper(hash_pre_final, hash_val)
    return final_hash


def hmac_verify(k, iv, message, tag):
    """Verification algorithm for hmac

    Args:
        k (binary string n bits): key for hmac
        iv (binary string n bits): Initialization vector
        message (binary string): message whose tag will be calculated
        tag (binary string n bits): Tag send to reciever for verification

    Returns:
        boolean: True if tag verified else False
    """
    gen_tag = hmac(k, iv, message)
    if gen_tag == tag:
        return True
    else:
        return False


# set global parameters
p, q, g, h = get_group_parameters()


def start():
    SIZE = 16
    iv = dec_to_bin(getrandbits(SIZE), SIZE)
    message = str(input('Enter message in string like Hello world\n'))
    message_bin = str_to_bin(message)
    print(f"Binary message:\n{message_bin}")
    key = input('Enter key for MAC < 16 bits in binary\n')
    key = key.zfill(SIZE)
    tag = hmac(key, iv, message_bin)
    print(f"Generated Tag:\n{tag}")
    if hmac_verify(key, iv, message_bin, tag):
        print("MAC verified")
    else:
        print("MAC compromised")


start()
