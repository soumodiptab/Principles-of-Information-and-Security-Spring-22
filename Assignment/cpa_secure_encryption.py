from pseudo_random_function import *
# using output feedback mode
# we should have a private key that we will use on both sides
# r will be our nonce
PRIVATE_KEY = '10110101001100'.zfill(16)
CHUNK_LENGTH = SEED_SIZE*2

def xor(bin_x, bin_y):
    return "".join(str(ord(x) ^ ord(y)).replace('0b', '') for x, y in zip(bin_x, bin_y))


def encrypt(nonce, message):
    # padding_size = len(message) + (CHUNK_LENGTH - len(message) % CHUNK_LENGTH)
    # message = message.zfill(padding_size)
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
    return r, cipher_text


def decrypt(r, cipher_text):
    propagator = r
    message = []
    # print("decrypt: ")
    for cipher in cipher_text:
        propagator = F(PRIVATE_KEY, propagator)
        # print(propagator)
        message_block = xor(propagator, cipher)
        message.append(message_block)
    return ''.join(message)


def test():
    orig_message = "100001000101111000001001"
    r, c = encrypt("10110110".zfill(16), orig_message)
    #print(f"r= {r}\ncipher= {c}\n")
    m = decrypt(r, c)
    #print(f"m= {m}")
    if orig_message == m:
        print("CPA working")
    else:
        print("Not Working")
test()