from pseudo_random_function import F
from crypto_utils import *
# own library


def mac(k, message, chunk_length):
    #work in progress
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
    r = get_random_bits(frag)
    l = bin(len(message)).replace('0b', '').zfill(frag)
#    for i in range(len(chunks)):


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
        return True
    return False


def test():
    test_key = get_random_bits(16)
    test_message = "1001110000100111111000111000111101"
    # bit_encoded_message=test_mesage.encode()
    cbc = cbc_mac(test_key, test_message)
    if cbc_mac_verify(test_key, test_message, cbc):
        print('Works')
    else:
        print('Doesnt work')


test()
