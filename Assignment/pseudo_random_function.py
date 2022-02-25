from pseudo_random_gen import *

def F(k, x):
    """F : Pseudo random function

    Args:
        k (string): seed (length - 16 bits)
        x (string): input string
    """
    # generate random seed of 2n bits
    seed = k.zfill(len(k))
    for i in range(len(x)):
        first, last = split_string(seed)
        if int(x[i]) == 0:
            seed = gen(first)
        else:
            seed = gen(last)
    return seed


# print(F("11010101".zfill(16), "11011001"))
