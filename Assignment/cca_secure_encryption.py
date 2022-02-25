from pseudo_random_function import *
from crypto_utils import xor, get_random_bits
# using output feedback mode
# we should have a private key that we will use on both sides
# r will be our nonce


def xor(bin_x, bin_y):
    return "".join(str(ord(x) ^ ord(y)).replace('0b', '') for x, y in zip(bin_x, bin_y))


def Encrypt(k1, k2, message, CHUNK_LENGTH, PRIVATE_KEY):


def encrypt(nonce, message, CHUNK_LENGTH, PRIVATE_KEY):
    chunks = [message[i:i+CHUNK_LENGTH]
              for i in range(0, len(message), CHUNK_LENGTH)]
    # nonce
    r = gen(nonce.zfill(len(nonce)), singler)
    propagator = r
    cipher_text = []
    # print("encrypt: ")
    for chunk in chunks:
        propagator = F(PRIVATE_KEY, propagator)
        # print(propagator)
        cipher = xor(propagator, chunk)
        cipher_text.append(cipher)
    return r, ''.join(cipher_text)


def decrypt(r, cipher_text, PRIVATE_KEY, CHUNK_LENGTH):
    propagator = r
    chunks = [cipher_text[i:i+CHUNK_LENGTH]
              for i in range(0, len(cipher_text), CHUNK_LENGTH)]
    message = []
    # print("decrypt: ")
    for cipher in chunks:
        propagator = F(PRIVATE_KEY, propagator)
        # print(propagator)
        message_block = xor(propagator, cipher)
        message.append(message_block)
    return ''.join(message)


def Gen(init, size):
    key1 = PRG_single(init)
    key2 = PRG_single(init)
    return key1, key2


def test():
    PRIVATE_KEY = get_random_bits(16)
    CHUNK_LENGTH = len(PRIVATE_KEY)
    # own library that generates random bits using pseudo random generator
    nonce = get_random_bits(16)
    orig_message = "100001000101111000001001"
    r, c = encrypt(nonce, orig_message, CHUNK_LENGTH, PRIVATE_KEY)
    #print(f"r= {r}\ncipher= {c}\n")
    m = decrypt(r, c)
    #print(f"m= {m}")
    if orig_message == m:
        print("CPA working")
    else:
        print("Not Working")


test()
