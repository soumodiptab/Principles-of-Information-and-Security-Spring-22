from crypto_utils import bin_to_dec, dec_to_bin, split_text, add_zeros_at_end, xor
from random import randint
import math
# Building a Hash Function with the help of Discrete log


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


def get_group_parameters():
    p = 65521
    q = (p-1)//2
    g = generator(q)
    h = randint(0, q-1)
    while h == g:
        h = randint(0, q-1)
    return p, q, g, h


def hash(x1, x2, g, h, p):
    return (pow(g, x1, p)*pow(h, x2, p)) % p


def hash_wrapper(x1, x2, g, h, p):
    x1_dec = bin_to_dec(x1)
    x2_dec = bin_to_dec(x2)
    return dec_to_bin(hash(x1_dec, x2_dec, g, h, p), len(x1))


def merkle_damgard(iv, message, p, q, g, h):
    SIZE = len(iv)
    encoded_size = dec_to_bin(len(message), SIZE)
    messages = split_text(message, SIZE)
    messages[-1] = add_zeros_at_end(messages[-1], SIZE)
    messages.append(encoded_size)
    x1 = iv
    for m in messages:
        x2 = m
        x1 = hash_wrapper(x1, x2, g, h, p)
    return dec_to_bin(x1, SIZE)


def repeat_string(inp, length):
    l = len(inp)
    mult = math.ceil(length/l)
    return mult*inp


def hmac(k, iv, message):
    SIZE = len(iv)
    ipad = dec_to_bin(0x34, SIZE)
    opad = dec_to_bin(0x5C, SIZE)
    ipad_repeat = repeat_string(ipad, len(k))
    opad_repeat = repeat_string(opad, len(k))
    xored_ipad = xor(k, ipad_repeat)
    xored_opad = xor(k, opad_repeat)
    hash_init = hash_wrapper(iv, xored_ipad, g, h, p)
    hash_pre_final = hash_wrapper(iv, xored_opad, g, h, p)
    hash_val = merkle_damgard(hash_init, message, p, q, g, h)
    final_hash = hash_wrapper(hash_pre_final, hash_val, g, h, p)
    return final_hash


def hmac_verify(iv, message):
    pass


def hash_demo():
    p, q, g, h = get_group_parameters()
    x1 = randint(0, q-1)
    x2 = randint(0, q-1)
    if x1 == x2:
        x2 = randint(0, q-1)
    print(x1)
    print(x2)
    hash_val = hash(x1, x2, g, h, p)
    print(hash_val)


p, q, g, h = get_group_parameters()

hash_demo()
