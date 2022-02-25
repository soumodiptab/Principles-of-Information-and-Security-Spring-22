from random import randint, getrandbits
from tarfile import BLOCKSIZE

# Building a Hash Function with the help of Discrete log
BLOCK_SIZE = 16
q = 582839576166181962101771435851
p = 2*q+1
# convert dec to binary


def dec_to_bin(x, size):
    return bin(x).zfill(size)
# convert binary to dec


def bin_to_dec(x):
    return int(x, 2)


def xor(bin_x, bin_y):
    return "".join(str(ord(x) ^ ord(y)).replace('0b', '') for x, y in zip(bin_x, bin_y))


def split_text(message, block_size):
    chunks = [message[i:i+block_size]
              for i in range(0, len(message), block_size)]
    return chunks
# generate group parameters G: q,g,h


def gen_prime(size):
    pass


def generator(q):
    p = 2*q+1
    while True:
        g = randint(2, p-1)
        if pow(g, q, p) != 1 and pow(g, 2, p) != 1:
            break
    return g


def Hash(string):
    pass


def merkle_damgard(iv, message, p):
    return merkle_damgard(iv, message, p, len(message))


def merkle_damgard(iv, message, p, last):
    SIZE = len(iv)
    messages = split_text(message, SIZE)
#    for m in messages
print(xor('10001','1110'))