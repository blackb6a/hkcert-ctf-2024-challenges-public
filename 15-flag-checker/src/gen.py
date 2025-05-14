from functools import reduce
from Crypto.Util.number import getPrime
import os
MAX_LENGTH = 128
def chinese_remainder(m, a):
    sum = 0
    prod = reduce(lambda acc, b: acc*b, m)
    for n_i, a_i in zip(m, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1
 
def ehcf(a,b):
    # Initialization
    p1 = 1
    q1 = 0
    h1 = a
    p2 = 0
    q2 = 1
    h2 = b
    
    # Loop
    while h2 != 0:
        r = h1//h2
        p3 = p1 - r*p2
        q3 = q1 - r*q2
        h3 = h1 - r*h2
        p1 = p2
        q1 = q2
        h1 = h2
        p2 = p3
        q2 = q3
        h2 = h3
    # Output
    return [p1, q1, h1]

def solve(m, a , b):
    _a0 = ehcf(b[0],m[0])[0] * a[0] % m[0]
    _a1 = ehcf(b[1],m[1])[0] * a[1] % m[1]
    _a = [_a0,_a1]
    return chinese_remainder(m,_a)

flag = "hkcert24{51mpl3_l1n34r_c0n6ru3nc35_50lv3d_w17h_cr7_65894851}"
flag = flag + "0"*(MAX_LENGTH-(len(flag)))
m_t = []
a_t = []
b_t = []
for idx in range(0,len(flag),4):
    p = getPrime(32,os.urandom)
    q = getPrime(32,os.urandom)
    m = [p, q]
    f = flag[idx:idx+4]
    b1 = getPrime(32,os.urandom)
    b2 = getPrime(32,os.urandom)
    b = [b1,b2]
    c = int("".join(hex(ord(i))[2:] for i in f),16)
    a1 = (c * b1) % p
    a2 = (c * b2) % q
    a = [a1,a2]
    m_t.append(m)
    a_t.append(a)
    b_t.append(b)
    assert(solve(m, a, b) == c)

print(f"unsigned long long m[{len(m_t)}][{len(m_t[0])}] = {str(m_t).replace('[','{').replace(']','}')};\nunsigned long long a[{len(a_t)}][{len(a_t[0])}] = {str(a_t).replace('[','{').replace(']','}')};\nunsigned long long b[{len(b_t)}][{len(b_t[0])}] = {str(b_t).replace('[','{').replace(']','}')};\n")
print(f"m_t = {str(m_t)}\na_t = {str(a_t)}\nb_t = {str(b_t)}\n")