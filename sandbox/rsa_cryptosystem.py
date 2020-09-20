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
        q = divmod(u, v)[0]
        u1, v1 = v1, u1 - v1 * q
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
    # if not isinstance(s, bytes): s = unidecode(str(s)).encode('utf-8')
    if not isinstance(s, bytes): s = str(s).encode('utf-8')
    length = len(s)
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





def encryptDataFrame():
    import Crypto.Util.number
    from Crypto.PublicKey import RSA
    from unidecode import unidecode
    import pandas as pd
    import numpy as np
    import datetime
    import base64
    from tqdm import tqdm

    # pd.set_option('max_colwidth', None)

    def encrypt(msg, public_key):
        if not msg:
            return None
        encrypted_msg = public_key.encrypt(str(msg).encode('utf-8'), 32)[0]
        return base64.b64encode(encrypted_msg).decode('utf-8', errors='ignore')
        
    def decrypt(encrypted_msg, private_key):
        if not encrypted_msg:
            return None
        decoded_encrypted_msg = base64.b64decode(encrypted_msg)
        return private_key.decrypt(decoded_encrypted_msg).decode('utf-8', errors='ignore')
        
    def rsa_encrypt_df(df, variaveis, bits=2048, backup=True):
        key = Crypto.PublicKey.RSA.generate(bits) # generate pub and private key
        publickey = key.publickey() # public key export for exchange

        df = df.copy()
        t_s = datetime.datetime.now()
        if isinstance(variaveis, str): variaveis = [variaveis]
        for var in variaveis:
            df[var] = np.where(df[var].isna(), None, df[var])
            df[var] = df[var].apply(encrypt, args=(key,), convert_dtype=False)
        return df, key

    def rsa_decrypt_df(df, variaveis, key):
        import Crypto.Util.number
        df = df.copy()
        if isinstance(variaveis, str): variaveis = [variaveis]
        for var in variaveis:
            df[var] = np.where(df[var].isna(), None, df[var])
            df[var] = df[var].apply(decrypt, args=(key,), convert_dtype=False)
        return df
    
    variaveis = ['id', 'host_name', 'name', 'room_type']
    df = pd.read_csv("C:/Users/genic/Downloads/listings.csv")

    d_s = datetime.datetime.now()
    df_encrypted, k = rsa_encrypt_df(df, variaveis)
    print("Tempo de execução:", datetime.datetime.now() - d_s)

    print(f"{k.publickey().exportKey()}\n\n{k.exportKey()}")
    df_encrypted[variaveis]

    d_s = datetime.datetime.now()
    df_decrypted = rsa_decrypt_df(df_encrypted, variaveis, k)
    print("Tempo de execução:", datetime.datetime.now() - d_s)

    for var in variaveis:
        df[var] = df[var].astype(str)
        df_decrypted[var] = df_decrypted[var].astype(str)

    df_merge = df_decrypted[variaveis].merge(df[variaveis].assign(flag=1), on=variaveis, how='left')
    if df_merge.shape[0] == df_decrypted.shape[0]:
        print("Sucesso")
    else:
        print("Erro")
        print("Qtd. registros diferentes:", df_merge[df_merge['flag'].isna()].shape[0])
    df_decrypted[variaveis]




class RSAKey:
    def __init__(self, anotherKey=None, bits=2048, p=None, q=None, u=None, d=None, e=2**16+1, n=None, prime_false_positive_prob=1e-12): 
        import Crypto.Util.number
        if isinstance(anotherKey, RSAKey):
            for attr in anotherKey.__dict__.keys():
                setattr(self, attr, getattr(anotherKey, attr))
        elif isinstance(anotherKey, dict):
            for attr in anotherKey.keys():
                setattr(self, attr, anotherKey[attr])
        else:
            self.bits = bits
            self.e = e
            self.prime_false_positive_prob = prime_false_positive_prob

            self.p = p if p else Crypto.Util.number.getStrongPrime(self.bits, e=self.e, false_positive_prob=self.prime_false_positive_prob)
            self.q = q if q else Crypto.Util.number.getStrongPrime(self.bits - (self.bits>>1), e=self.e, false_positive_prob=self.prime_false_positive_prob)
            (self.p, self.q) = (self.q, self.p) if self.p > self.q else (self.p, self.q)

            self.u = u if u else Crypto.Util.number.inverse(self.p, self.q) # or inverse(p, q)
            self.n = n if n else self.p * self.q
            self.phi = (self.p - 1) * (self.q - 1)

            self.d = d if d else Crypto.Util.number.inverse(self.e, self.phi) # or inverse(e, phi)

    def hasPrivateKey(self):
        return hasattr(self, 'd')

    def hasPublicKey(self):
        return not self.hasPrivateKey()

    def exportPrivateKey(self):
        return {'p': self.p, 'q': self.q, 'd': self.d, 'u': self.u}
    
    def exportPublicKey(self):
        return {'n': self.n, 'e': self.e}
        
    def exportKey(self):
        return self.__dict__

    def encrypt(self, x):
        """
        Encripta o número x.

        Params:
            x: Número inteiro a ser criptografado. Ideal para chaves identificadoras, por exemplo.
        
        Return:
            Retorna um valor encriptado de `x`.
        """
        if not x:
            return None
        return pow(x, self.e, self.n) # x**e % n
    
    def decrypt(self, x):
        """
        Decripta o número x.

        Params:
            x: Número inteiro criptografado.
        
        Return:
            Retorna o valor decriptado de `x` se a chave atual for uma chave privada.
        """
        if not hasattr(self, 'd'): # if not has private key return
            raise Exception("Sorry! Private key is necessary!")
        if hasattr(self, 'p') and hasattr(self, 'q') and hasattr(self, 'u'): 
            m1 = pow(x, self.d % (self.p - 1), self.p)
            m2 = pow(x, self.d % (self.q - 1), self.q)
            h = m2 - m1
            if h < 0: h += self.q
            h = h * self.u % self.q
            return h * self.p + m1
        return pow(x, self.d, self.n)
