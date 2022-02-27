from pseudo_random_gen import PRG_single, gen, split_string
from cpa_secure_encryption import encrypt, decrypt
from message_authentication_code import cbc_mac, cbc_mac_verify
from crypto_utils import get_random_bits
# using output feedback mode
# we should have a private key that we will use on both sides
# r will be our nonce


def Gen(init):
    key = gen(init)
    init1, init2 = split_string(key)
    key1 = PRG_single(init1)
    key2 = PRG_single(init2)
    return key1, key2


def Encrypt(k1, k2, message, CHUNK_LENGTH, PRIVATE_KEY):
    r, c = encrypt(k1, message, CHUNK_LENGTH, PRIVATE_KEY)
    tag = cbc_mac(k2, c)
    return r, c, tag


def Decrypt(r, k2, cipher, CHUNK_LENGTH, PRIVATE_KEY, tag):
    assert cbc_mac_verify(
        k2, cipher, tag), "Compromised message, Tag Mismatch"
    m = decrypt(r, cipher, CHUNK_LENGTH, PRIVATE_KEY)
    return m


def test():
    init_vector = get_random_bits(16)
    PRIVATE_KEY = get_random_bits(16)
    CHUNK_LENGTH = len(PRIVATE_KEY)
    # own library that generates random bits using pseudo random generator
    orig_message = "100001000101111000001001"
    k1, k2 = Gen(init_vector)

    r, c, tag = Encrypt(k1, k2, orig_message, CHUNK_LENGTH, PRIVATE_KEY)
    #print(f"r= {r}\ncipher= {c}\n")
    m = Decrypt(r, k2, c, CHUNK_LENGTH, PRIVATE_KEY, tag)
    #print(f"m= {m}")
    if orig_message == m:
        print("CCA working")
    else:
        print("Not Working")


test()
