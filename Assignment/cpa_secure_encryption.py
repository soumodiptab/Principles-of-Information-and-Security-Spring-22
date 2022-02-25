from pseudo_random_function import F, PRG_single
from crypto_utils import get_random_bits, xor
# using output feedback mode
# we should have a private key that we will use on both sides
# r will be our nonce
# PRIVATE_KEY = '10110101001100'.zfill(16)
# CHUNK_LENGTH = SEED_SIZE*2

# def xor(bin_x, bin_y):
#     return "".join(str(ord(x) ^ ord(y)).replace('0b', '') for x, y in zip(bin_x, bin_y))


def encrypt(nonce, message, CHUNK_LENGTH, PRIVATE_KEY):
    chunks = [message[i:i+CHUNK_LENGTH]
              for i in range(0, len(message), CHUNK_LENGTH)]
    # nonce
    r = PRG_single(nonce.zfill(len(nonce)))
    propagator = r
    cipher_text = []
    # print("encrypt: ")
    for chunk in chunks:
        propagator = F(PRIVATE_KEY, propagator)
        # print(propagator)
        cipher = xor(propagator, chunk)
        cipher_text.append(cipher)
    return r, ''.join(cipher_text)


def decrypt(r, cipher_text, CHUNK_LENGTH, PRIVATE_KEY):
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


def test():
    PRIVATE_KEY = get_random_bits(16)
    CHUNK_LENGTH = len(PRIVATE_KEY)
    # own library that generates random bits using pseudo random generator
    nonce = get_random_bits(16)
    orig_message = "100001000101111000001001"
    r, c = encrypt(nonce, orig_message, CHUNK_LENGTH, PRIVATE_KEY)
    #print(f"r= {r}\ncipher= {c}\n")
    m = decrypt(r, c, CHUNK_LENGTH, PRIVATE_KEY)
    #print(f"m= {m}")
    if orig_message == m:
        print("CPA working")
    else:
        print("Not Working")


test()
