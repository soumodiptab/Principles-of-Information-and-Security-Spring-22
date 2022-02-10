from pseudo_random_function import *


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


def cbc_mac(message):
    l=len(message)
    
