from random import randint, getrandbits
# Building a Hash Function with the help of Discrete log
BLOCK_SIZE = 16
p = 582839576166181962101771435851
q = (p-1)/2
# convert dec to binary


def add_zeros_at_end(string, padding_size):
    return string[::-1].zfill(padding_size)[::-1]


def add_zeros_at_front(string, padding_size):
    return string.zfill(padding_size)


def dec_to_bin(x, size):
    return bin(x).replace('0b', '').zfill(size)
# convert binary to dec


def bin_to_dec(x):
    return int(x, 2)


def xor(bin_x, bin_y):
    return "".join(str(ord(x) ^ ord(y)).replace('0b', '') for x, y in zip(bin_x, bin_y))


def split_text(message, block_size):
    chunks = [message[i:i+block_size]
              for i in range(0, len(message), block_size)]
    return chunks


def gen_prime(size):
    pass


def generator(q):
    p = 2*q+1
    while True:
        g = randint(2, p-1)
        if pow(g, q, p) == 1 or pow(g, 2, p) == 1:
            continue
        else:
            break
    return g

# hash using DLP


def hash(x1, x2, g, h, p):
    return pow(g, x1, p)*pow(h, x2, p)


def merkle_damgard(iv, message, q):
    return merkle_damgard(iv, message, q, len(message))


def merkle_damgard(iv, message, p, q, g, h):
    SIZE = len(iv)
    encoded_size = dec_to_bin(SIZE, SIZE)
    messages = split_text(message, SIZE)
    messages[-1] = add_zeros_at_end(messages[-1])
    messages.append(encoded_size)
    x1 = iv
    for x2 in messages:
        x1 = hash(x1, x2, g, h, p)
    return x1


def hash_demo():
    bits = int(input('Enter number of bits >>\n'))
