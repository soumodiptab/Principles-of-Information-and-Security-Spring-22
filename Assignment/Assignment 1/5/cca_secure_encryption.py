import time

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


def PRG_single(x):
    """ PRG of same bit size"""
    return gen(x, p=singler)


def PRG_double(x):
    """PRG of double bit size"""
    return gen(x, p=doubler)


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


def xor(bin_x, bin_y):
    '''
    xor of the two binary strings
    '''
    return "".join(str(ord(x) ^ ord(y)).replace('0b', '') for x, y in zip(bin_x, bin_y))


def str_to_bin(s):
    return dec_to_bin_wo_pad(int.from_bytes(s.encode(), 'big'))


def bin_to_str(n):
    x = bin_to_dec(n)
    return x.to_bytes((x.bit_length() + 7) // 8, 'big').decode()


def encrypt(nonce, message, CHUNK_LENGTH, PRIVATE_KEY):
    """Encrypts binary message in CPA secure encryption in OFB mode
    Args:
        nonce (binary string - n bits): (also called IV) random initial value taken only once
        message (binary string): Message to be transmitted
        CHUNK_LENGTH (int): Size of message fragment
        PRIVATE_KEY (binary string - n bits): Private shared key
    Returns
        r – initialization vector, will be used at decryption
        c - binary string : Encrypted message
    """
    assert CHUNK_LENGTH <= len(message), "Fragment error"
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
    """Decrypts the cipher text into plain text in OFB mode

    Args:
        r (binary string - n bits): Used for decryption 
        cipher_text (binary string): Cipher text to be deciphered
        CHUNK_LENGTH (int): Size of message fragment
        PRIVATE_KEY (binary string - n bits): Private shared key

    Returns:
        binary string : Decrypted message
    """
    assert CHUNK_LENGTH <= len(cipher_text), "Fragment error"
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


def get_random_bits(size):
    '''
    Generate random binary string of specified bits
    '''
    now = (round(time.time() * 1000)) % (2**size)
    in_binary = dec_to_bin(now, size)
    random_identifier = gen(in_binary, singler)
    return random_identifier


def cbc_mac(k, message):
    """Calculates MAC tag using Cipher Block Chaining
    Args:
        k (binary string - n bits): input key for PRF in cbc MAC
        message (binary string): string for which tag needs to be calculated

    Returns:
        binary string - n bits: Tag of n bits
    """
    SIZE = len(k)
    message_size = bin(len(message)).replace('0b', '').zfill(SIZE)
    tag = F(k, message_size)
    chunks = [message[i:i+SIZE]for i in range(0, len(message), SIZE)]
    for m in chunks:
        xored_message = xor(tag, m)
        tag = F(k, xored_message)
    return tag


def cbc_mac_verify(k, message, tag):
    """Verifies the given tag with the original message

    Args:
        k (binary string - n bits): input key for PRF in cbc MAC
        message (binary string): string for which tag needs to be calculated
        tag (binary string - n bits): tag of n bits generated at sender

    Returns:
        boolean: True if tag matches the message else False
    """
    generated_tag = cbc_mac(k, message)
    if generated_tag == tag:
        return True
    return False

def Gen(init):
    """Generates two keys of length len(init)
    Working:
        uses a length doubling PRG to generate 2n bits and then, applies PRG on each part to obtain two keys
    Args:
        init (binary string - n bits): intitialization vector

    Returns:
        two binary strings: Returns two keys one for encryption and another for mac
    """
    key = gen(init)
    init1, init2 = split_string(key)
    key1 = PRG_single(init1)
    key2 = PRG_single(init2)
    return key1, key2


def Encrypt(k1, k2, message, CHUNK_LENGTH, PRIVATE_KEY):
    """CCA Encryption Function
    Working:
        Uses encrypt() to generate cipher text and applies cbc mac on the cipher text
    Args:
        k1 (binary string - n bits): Key for CPA Encryption
        k2 (binary string - n bits): Key for CBC MAC
        message ( binarys string): message to be encrypted
        CHUNK_LENGTH (int): Message Fragment size
        PRIVATE_KEY (binary string - n bits): Private key chosen
    Returns:
        r(binary string - n bits): generated random bits after encryption using key k1
        c(binary string): cipher text
        tag(binary string nbits): tag for mac
    """
    r, c = encrypt(k1, message, CHUNK_LENGTH, PRIVATE_KEY)
    tag = cbc_mac(k2, c)
    return r, c, tag


def Decrypt(r, k2, cipher, CHUNK_LENGTH, PRIVATE_KEY, tag):
    """Decryption using CPA decryptor and CBC MAC validator
    Working:
        Applies cbc_mac_verify on cipher text using key k2 and tag, and then decrypts only if mac verifies
    Args:
        r (binary string - n bits): key for CPA decryption
        k2 (binary string - n bits): Key for CBC MAC
        message ( binary string): message to be encrypted
        CHUNK_LENGTH (int): Message Fragment size
        PRIVATE_KEY (binary string - n bits): Private key chosen
        tag (binary string - n bits): tag for mac verification

    Returns:
        binary string : decrypted message
    """
    assert cbc_mac_verify(
        k2, cipher, tag), "Compromised message, Tag Mismatch"
    m = decrypt(r, cipher, CHUNK_LENGTH, PRIVATE_KEY)
    return m


def start():
    PRIVATE_KEY = str(input('Enter Private key in binary(16 bit recommended)\n'))
    message = str(input('Enter message example: Hello world\n'))
    orig_message = str_to_bin(message)
    print('BINARY MESSAGE:\n', orig_message)
    CHUNK_LENGTH = int(input('Enter size of fragment\n'))
    init_vector = get_random_bits(CHUNK_LENGTH)
    print('Random init vector:\n', init_vector)
    k1, k2 = Gen(init_vector)
    r, c, tag = Encrypt(k1, k2, orig_message, CHUNK_LENGTH, PRIVATE_KEY)
    m = Decrypt(r, k2, c, CHUNK_LENGTH, PRIVATE_KEY, tag)
    print('Encrypted message:\n', c)
    print('Decrypted message:\n', m)
    if orig_message == m:
        print("CCA working")
        print('Decrypted message:\n', bin_to_str(m))
    else:
        print("CCA Not Working")

start()
