from pseudo_random_function import *
# using output feedback mode
# we should have a private key that we will use on both sides
# r will be our nonce
PRIVATE_KEY = '10110101'
CHUNK_LENGTH = SEED_SIZE*2


def xor(x, y):
    max_length = max(len(x), len(y))
    x = x.zfill(max_length)
    y = y.zfill(max_length)
    result = ""
    for i in range(max_length):
        result += str(int(x[i]) ^ int(y[i]))
    return result


def encrypt(nonce, message):
    padding_size = len(message) + (CHUNK_LENGTH - len(message) % CHUNK_LENGTH)
    message = message.zfill(padding_size)
    chunks = [message[i:i+CHUNK_LENGTH]
              for i in range(0, len(message), CHUNK_LENGTH)]
    # nonce
    r = gen(nonce.zfill(len(nonce)), singler)
    propagator = r
    cipher_text = []
    print("encrypt: ")
    for chunk in chunks:
        propagator = F(PRIVATE_KEY, propagator)
        print(propagator)
        cipher = xor(propagator, chunk)
        cipher_text.append(cipher)
    return r, cipher_text


def decrypt(r, cipher_text):
    propagator = r
    message = []
    print("decrypt: ")
    for cipher in cipher_text:
        propagator = F(PRIVATE_KEY, propagator)
        print(propagator)
        message_block = xor(propagator, cipher)
        message.append(message_block)
    return message


# r, c = encrypt("10110110".zfill(16), "1000010101000101111")
# print(f"r= {r}\ncipher= {c}\n")
# m = decrypt(r, c)
# print(f"m= {''.join(m)}")
