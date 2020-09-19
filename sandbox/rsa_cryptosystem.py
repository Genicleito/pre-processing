import Crypto.Util.number
import datetime

t_start = datetime.datetime.now()
timer = datetime.datetime.now()

def executionTime():
	"""Prints the time difference between start of the execution and current point
	"""
	print('Tempo de execucao ate este ponto: ' + str(datetime.datetime.now() - t_start))

def startTimer():
	"""Set the timer variable to present time.
	"""
	global timer
	timer = datetime.datetime.now()	

def printTimer():
	"""Prints the timer variable.
	"""
	print('Tempo de execucao: ' + str(datetime.datetime.now() - timer))


def inverse(u, v):
    """inverse(u:long, v:long):long
    Return the inverse of u mod v.
    
    Ref.: https://github.com/pycrypto/pycrypto
    """
    # u3, v3 = long(u), long(v)
    u1, v1 = 1, 0
    while v > 0:
        q=divmod(u, v)[0]
        u1, v1 = v1, u1 - v1*q
        u, v = v, u - v*q
    while u1 < 0:
        u1 = u1 + v
    return u1


def bytes_to_long(s):
    """bytes_to_long(string) : long
    Convert a byte string to a long integer.
    This is (essentially) the inverse of long_to_bytes().
    
    Ref.: Ref.: https://github.com/pycrypto/pycrypto
    """
    import struct
    from unidecode import unidecode
    
    acc = 0
    length = len(s)
    s = unidecode(s).encode('utf-8')
    if length % 4:
        extra = (4 - length % 4)
        s = '\000'.encode('utf-8') * extra + s
        length = length + extra
    for i in range(0, length, 4):
        acc = (acc << 32) + struct.unpack('>I', s[i:i+4])[0]
    return acc


def long_to_bytes(n, encoding='utf-8', blocksize=0):
    """long_to_bytes(n:long, blocksize:int) : string
    Convert a long integer to a byte string.
    If optional blocksize is given and greater than zero, pad the front of the
    byte string with binary zeros so that the length is a multiple of
    blocksize.
    
    Ref.: Ref.: https://github.com/pycrypto/pycrypto
    """
    # after much testing, this algorithm was deemed to be the fastest
    import struct
    s = ''.encode('utf-8')
    while n > 0:
        s = struct.pack('>I', n & 0xffffffff) + s
        n = n >> 32
    # strip off leading zeros
    for i in range(len(s)):
        if s[i] != '\000'.encode('utf-8')[0]:
            break
    else:
        # only happens when n == 0
        s = '\000'.encode('utf-8')
        i = 0
    s = s[i:]
    if blocksize > 0 and len(s) % blocksize:
        s = (blocksize - len(s) % blocksize) * '\000'.encode('utf-8') + s
    return s.decode(encoding) if encoding else s

def encrypt(x, e, n):
    return pow(x, e, n) # x**e % n

def decrypt(c, n, d, p=None, q=None, u=None):
    if not d: # if not has private key return - add this
        print("private key is necessary!")
        return None
    if p and q and u:
        m1 = pow(c, d % (p - 1), p)
        m2 = pow(c, d % (q - 1), q)
        h = m2 - m1
        if h < 0: h += q
        h = h * u % q
        return h * p + m1
    return pow(c, d, n)

def generateRSA(bits=2048, e=2**16+1, prime_false_positive_prob=1e-12):
    # bits = 2048
    # e = 2**16+1
    # t_s1 = datetime.datetime.now()
    p = Crypto.Util.number.getStrongPrime(bits, e=e, false_positive_prob=prime_false_positive_prob)
    # t_s2 = datetime.datetime.now()
    q = Crypto.Util.number.getStrongPrime(bits - (bits>>1), e=e, false_positive_prob=prime_false_positive_prob)
    # print("Tempo de execução p:", datetime.datetime.now() - t_s1)
    # print("Tempo de execução q:", datetime.datetime.now() - t_s2)

    (p, q) = (q, p) if p > q else (p, q)
    print(f"p: {p}\n\nq: {q}")

    u = Crypto.Util.number.inverse(p, q) # or inverse(p, q)
    n = p * q
    phi = (p - 1) * (q - 1)
    d = Crypto.Util.number.inverse(e, phi) # or inverse(e, phi)

    public_key = (n, e)
    private_key = (p, q, d, u)

    # print(f"Public key:\n\tn = {public_key[0]}\n\te = {public_key[1]}\n{125*'-'}\nPrivate key:\n\tp = {private_key[0]}\n\tq = {private_key[1]}\n\td = {private_key[2]}")

    # c = encrypt(32485, e, n)
    # decrypt(c, n, d)==32485

    return private_key, public_key