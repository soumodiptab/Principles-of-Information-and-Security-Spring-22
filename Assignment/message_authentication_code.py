from pseudo_random_function import *
from cpa_secure_encryption import xor


def mac(k, message):
    """mac finds the message authentication code

    Args:
        k (bin string): key of the session
        m (bin string): message
    """
    # should be multiple of 4
    CHUNK_LENGTH = len(k)
    FRAG = int(CHUNK_LENGTH/4)
    l = bin(len(message)).replace('0b', '').zfill(FRAG)
    padding_size = len(message) + (CHUNK_LENGTH - len(message) % CHUNK_LENGTH)
    message = message.zfill(padding_size)


def cbc_mac(k, message):
    SIZE = len(k)
    message_size = bin(len(message)).replace('0b', '').zfill(SIZE)
    tag = F(k, message_size)
    chunks = [message[i:i+SIZE]for i in range(0, len(message), SIZE)]
    for m in chunks:
        xored_message = xor(tag, m)
        tag = F(k, xored_message)
    return tag


def cbc_verify(k, message, tag):
    generated_tag = cbc_mac(k, message)
    if generated_tag == tag:
        return 1
    return 0

testing_cbc=cbc_mac("10001011",)