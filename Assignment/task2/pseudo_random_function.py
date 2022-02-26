GENERATOR = 8173
MOD = 65521


def split_string(x):
    '''
    splits string into two equal parts
    '''
    middle = int(len(x)/2)
    first = x[:middle]
    last = x[middle:]
    return first, last


def dec_to_bin_wo_pad(x):
    '''
    Converts decimal to binary without padding
    '''
    return bin(x).replace('0b', '')


def dec_to_bin(x, size):
    '''
    Converts decimal to binary with padding
    '''
    return bin(x).replace('0b', '').zfill(size)


def bin_to_dec(x):
    '''
    converts binary to decimal
    '''
    return int(x, 2)


def doubler(n):
    '''
    Polynomial to double the length
    '''
    return 2*n


def singler(n):
    '''
    Polynomial to keep length same
    '''
    return n

# this is our one-way function f(x)=discrete logarithm


def discrete_log(x):
    """
    DLP One way function
    GENERATOR = 8173
    MOD = 65521
    Args:
        x (int): seed value
    Returns:
        one way function value
    """
    return pow(GENERATOR, x, MOD)

# takes an input of size n returns of size n+1


def get_hardcore_bit(x):
    '''
    Extracts Hardcore bit using Blum Micali:
    if  x <  prime/2    - 0
        x >= prime/2    - 1
    '''
    if x < MOD//2:
        return 0
    else:
        return 1


def g(x):
    """
    Takes input binary string x( L bits) and return hardcore bit and new seed of L+1 bits
    """
    x_dec = bin_to_dec(x)
    val = discrete_log(x_dec)
    hc_bit = get_hardcore_bit(val)
    #val ^= x_dec
    return str(hc_bit), dec_to_bin(val, len(x))


def gen(x, p=doubler):
    """
    Pseudo Random number generator
    Args:
        x (binary string): Initial Seed
        p (function, optional): A polynomial input can be given. Defaults to doubler.
    Returns:
        (binary string): Pseudo random bits
    """
    length = p(len(x))
    result = ""
    seed = x
    for i in range(length):
        bit, seed = g(seed)
        result += bit
    return result


def F(k, x):
    """F : Pseudo random function
    Args:
        k (string): seed (length - n bits)
        x (string): input string
    Returns:
        n bit 
    """
    seed = k.zfill(len(k))
    for i in range(len(x)):
        first, last = split_string(seed)
        if int(x[i]) == 0:
            seed = gen(first)
        else:
            seed = gen(last)
    return seed


def start():
    key = str(input('Enter key in binary\n'))
    message = str(input('Enter message in binary\n'))
    val = F(key, message)
    print(f"Generated Bits using Pseudo Random Function:\n{val}")


start()
