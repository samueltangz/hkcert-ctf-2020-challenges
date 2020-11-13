# HKCERT CTF Challenge 2020 Writeup
### Team: T0077 - HKUST
### Challenge Name: Tenet 天能 (Crypto, 492 points)

Solved by _Vincent_
#first_blood

---

Objective: Given encryption code, decipher this:
`6255c24aa3dd8f58c5fcb41feb90f90e73e870db651d5a963498f062c2c1572430098acf05`

---

Observations: 

1. AES Double-Key Encryption:
$C=E(E(P, K_0, IV_0), K_1, IV_1)$
$P=D(D(C, K_1, IV_1), K_0, IV_0)$
$\Rightarrow$ Meet-in-the-middle attack?
$D(C, K_1, IV_1)=E(P, K_0, IV_0)$
2. The National Security Law in the near future requires first 13 bytes of keys to be zeros.
`key1 = b'\0' * 13 + os.urandom(3)`
`key2 = b'\0' * 13 + os.urandom(3)`
$\Rightarrow$ Key search space = $2^{24}$
3. Of course we don't know the whole plaintext, we just know it starts with `hkcert20{`. However, even having partial plaintext is useless for MiM attacks, unless...
4. `mode=AES.MODE_CTR`

$C_i=(P_i \oplus E_{CTR}(IV_0+i, K_0)) \oplus E_{CTR}(IV_1+i, K_1)\\
\ \ \ \ =P_i \oplus (E_{CTR}(IV_0+i, K_0) \oplus E_{CTR}(IV_1+i, K_1))$

$\Rightarrow P=C \oplus (E(\vec{0}, K_0, IV_0) \oplus E(\vec{0}, K_1, IV_1))$

---

Exhaust all $2^{24}$ keys, compute $E(\vec{0}, K, IV_0)$ and $E(\vec{0}, K, IV_1)$, label using the first 3 bytes of the keystreams.

Then $\forall K_0, K_1$ s.t. $E(E(P, K_0, IV_0), K_1, IV_1)$`[:3] == b'hkc'`, check if `[:9] == b'hkcert20{'`

---

```python=
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.number import bytes_to_long, long_to_bytes
import os

flaggie = b'hkcert20{'

ciphervalue = 0x6255c24aa3dd8f58c5fcb41feb90f90e73e870db651d5a963498f062c2c1572430098acf05
ciphertext = long_to_bytes(ciphervalue)

head = bytes_to_long(flaggie[:3]) ^ bytes_to_long(ciphertext[:3])

# In the future, we have not only time inversion but also quantum computers.
# So, we need to encrypt twice to double the key size.
class TenetAES():
    def __init__(self, key0, key1):
        self.aes128_0 = AES.new(key=key0, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=1))
        self.aes128_01 = AES.new(key=key0, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=1))
        self.aes128_1 = AES.new(key=key1, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=129))
        self.aes128_11 = AES.new(key=key1, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=129))

    def keystreams(self, n = 37):
        return self.aes128_0.encrypt(b'\0' * n), self.aes128_1.encrypt(b'\0' * n)

    def encrypt(self, s):
        n = len(s)
        x = self.aes128_1.encrypt(self.aes128_0.encrypt(s))
        y = long_to_bytes(
                bytes_to_long(self.aes128_01.encrypt(b'\0' * n)) 
                ^ bytes_to_long(self.aes128_11.encrypt(b'\0' * n)) 
                ^ bytes_to_long(s)
            ) 
        assert x == y
        return x

    def decrypt(self, data):
        n = len(data)
        x = self.aes128_0.decrypt(self.aes128_1.decrypt(data))
        y = long_to_bytes(
                bytes_to_long(self.aes128_01.encrypt(b'\0' * n)) 
                ^ bytes_to_long(self.aes128_11.encrypt(b'\0' * n)) 
                ^ bytes_to_long(data)
            ) 
        assert x == y
        return x

#with open('flag.txt') as f:
#    flag = f.read()

# The National Security Law in the near future requires first 13 bytes of
# keys to be zeros.

#key1 = b'\0' * 13 + os.urandom(3)
#key2 = b'\0' * 13 + os.urandom(3)

one = [[] for i in range(16777216)]
two = [[] for i in range(16777216)]

for i in range(16777216):
    key1 = b'\0' * 13 + i.to_bytes(3, byteorder = 'big')
    key2 = b'\0' * 13 + i.to_bytes(3, byteorder = 'big')
    a, b = TenetAES(key1, key2).keystreams()
    one[bytes_to_long(a[:3])].append(i)
    two[bytes_to_long(b[:3])].append(i)

for i in range(16777216):
    for a in one[i]:
        for b in two[i ^ head]:
            key1 = b'\0' * 13 + a.to_bytes(3, byteorder = 'big')
            key2 = b'\0' * 13 + b.to_bytes(3, byteorder = 'big')
            aa, bb = TenetAES(key1, key2).keystreams()
            aa = bytes_to_long(aa)
            bb = bytes_to_long(bb)
            x = (aa ^ bb ^ ciphervalue).to_bytes(37, byteorder='big')
            assert x[:3] == b'hkc'
            if x[:9] == flaggie:
                print(key1)
                print(key2)
                print(x)
```

```python
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00+!0'
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00&\x84\xd2'
b'hkcert20{7h3_b361nn1n6_15_7h3_3nd1n6}'
```

---

P.S.

![](https://i.imgur.com/39LHsr8.png)

P.P.S. Official Hint: (viewed after contest)
In "Tenet", red team and blue team meet in the middle.

---

###### _In memory of Neil_

