GENERATOR = 8173
MOD = 65521


def split_string(x):
    middle = int(len(x)/2)
    first = x[:middle]
    last = x[middle:]
    return first, last


def dec_to_bin_wo_pad(x):
    """dec_to_bin converts decimal to binary

    Args:
        x (int): integer

    Returns:
        str : binary string
    """
    return bin(x).replace('0b', '')


def dec_to_bin(x, size):
    '''
    convert decimal to binary
    '''
    return bin(x).replace('0b', '').zfill(size)


def bin_to_dec(x):
    return int(x, 2)


def doubler(n):
    return 2*n


def singler(n):
    return n

# this is our one-way function f(x)=discrete logarithm


def discrete_log(x):
    return pow(GENERATOR, x, MOD)

# takes an input of size n returns of size n+1


def get_hardcore_bit(x):
    if x < MOD//2:
        return 0
    else:
        return 1


def g(x):
    x_dec = bin_to_dec(x)
    val = discrete_log(x_dec)
    hc_bit = get_hardcore_bit(val)
    #val ^= x_dec
    return str(hc_bit), dec_to_bin(val, len(x))


def gen(x, p=doubler):
    length = p(len(x))
    result = ""
    seed = x
    for i in range(length):
        bit, seed = g(seed)
        result += bit
    return result


def PRG_single(x):
    return gen(x, p=singler)


# test_string = get_random_bits(8)
# print(gen(test_string))
