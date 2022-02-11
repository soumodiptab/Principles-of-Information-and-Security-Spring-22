from pseudo_random_function import *
from cpa_secure_encryption import xor
import time


def to_binary(number, size):
    return bin(number).replace('0b', '').zfill(size)


def get_random_identifier(size):
    now = (round(time.time() * 1000)) % (2**size)
    in_binary = to_binary(now, size)
    random_identifier = gen(in_binary, singler)
    return random_identifier


def mac(k, message, chunk_length):
    """mac finds the message authentication code
    Args:
        k (bin string): key of the session
        message (bin string): message
        chunk_length(int): size of each mac
    """
    # should be multiple of 4
    frag = int(chunk_length/4)
    chunks = [message[i:i+frag]for i in range(0, len(message), frag)]
    tags = []
    r=get_random_identifier(frag)
    l=bin(len(message)).replace('0b', '').zfill(frag)
    for i in range(len(chunks)):
        
       




def cbc_mac(k, message):
    SIZE = len(k)
    message_size = bin(len(message)).replace('0b', '').zfill(SIZE)
    tag = F(k, message_size)
    chunks = [message[i:i+SIZE]for i in range(0, len(message), SIZE)]
    for m in chunks:
        xored_message = xor(tag, m)
        tag = F(k, xored_message)
    return tag


def cbc_mac_verify(k, message, tag):
    generated_tag = cbc_mac(k, message)
    if generated_tag == tag:
        return 1
    return 0


testing_cbc = cbc_mac("10001011".zfill(
    16), "1001110000100111111000111000111101")

print(cbc_mac_verify("10001011".zfill(16),
      "1001110000100111111000111000111101", testing_cbc))
print(get_random_identifier(16))