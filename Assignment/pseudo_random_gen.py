SEED_SIZE = 8
GENERATOR = 223
MOD = 36389


def split_string(x):
    middle = int(len(x)/2)
    first = x[:middle]
    last = x[middle:]
    return first, last


def doubler(n):
    return 2*n


def singler(n):
    return n
# this is our one-way function f(x)=discrete logarithm


def f(x):
    return bin(pow(GENERATOR, int(x, 2), MOD)).replace('0b', '').zfill(SEED_SIZE)

# takes an input of size n returns of size n+1


def g(x):
    first, last = split_string(x)
    gen = f(first)
    hc_bit = 0
    for i in range(len(first)):
        hc_bit = (hc_bit ^ (int(first[i]) & int(last[i])))
    return gen + last + str(hc_bit)


def gen(x, p=doubler):
    length = p(len(x))
    result = ""
    seed = x
    for i in range(length):
        seed = g(seed)
        result += seed[-1]
    return result


# test_string = "1000011"
# seed = test_string.zfill(SEED_SIZE)
# print(gen(seed))
