from pwn import *
from math import gcd
from Crypto.Util.number import isPrime as is_prime


def attempt(id):
    e = 65537

    log.info(f'attempt #{id}')

    # r = process(['python3', 'chall.py'])
    r = remote('localhost', 28134)

    r.recvuntil(b'c = ')
    c0 = int(r.recvline().decode())

    r.sendline(b'p')
    r.sendline(b'q')
    r.sendline(b'p+q')

    r.recvuntil(b'Input your expression in terms of p, q and r: ')
    s1 = int(r.recvline().decode()) # a := p^e mod n
    r.recvuntil(b'Input your expression in terms of p, q and r: ')
    s2 = int(r.recvline().decode()) # b := q^e mod n
    r.recvuntil(b'Input your expression in terms of p, q and r: ')
    s3 = int(r.recvline().decode()) # c := (p^e + q^e) mod n

    # s1 and s2 are of different lengths
    if set([len(str(s1)), len(str(s2))]) != set([154, 155]):
        r.close()
        return False
    
    # Require that a + b = c
    if len(str(s3)) != 155:
        r.close()
        return False

    if len(str(s1)) < len(str(s2)):
        # p < q
        s1, s2 = s2, s1
        r.sendline(b'q-p')
        r.sendline(b'p+p')
        r.sendline(b'-q%p')
    else:
        # p > q
        r.sendline(b'p-q')
        r.sendline(b'q+q')
        r.sendline(b'-p%q')

    # Nonetheless, we have p > q now.

    r.recvuntil(b'Input your expression in terms of p, q and r: ')
    s4 = int(r.recvline().decode()) # s4 := (p^e - q^e) mod n
    r.recvuntil(b'Input your expression in terms of p, q and r: ')
    s5 = int(r.recvline().decode()) # s5 := (2^e q^e) mod n
    r.recvuntil(b'Input your expression in terms of p, q and r: ')
    s6 = int(r.recvline().decode()) # s6 := (-p^e - 2^e q^e) mod n

    if len(str(s4)) != 154:
        r.close()
        return False

    if len(str(s5)) != 155:
        r.close()
        return False
    if len(str(s6)) != 154:
        r.close()
        return False

    _a = [None for _ in range(309)]
    _b = [None for _ in range(309)]
    _s = [None for _ in range(309)] # a+b
    _d = [None for _ in range(309)] # a-b
    _c = [None for _ in range(309)] # c
    _f = [None for _ in range(309)] # c-a

    for i in range(155): _a[2*i+0] = int(str(s1)[i])
    for i in range(154): _b[2*i+1] = int(str(s2)[i]); _b[0] = 0
    for i in range(155): _s[2*i+0] = int(str(s3)[i])
    for i in range(154): _d[2*i+1] = int(str(s4)[i]); _d[0] = 0
    for i in range(155): _c[2*i+0] = int(str(s5)[i])
    for i in range(154): _f[2*i+1] = int(str(s6)[i]); _f[0] = 0
    
    assert _a[0] == 1

    a = b = s = d = 0
    for i in range(308, 0, -2):
        # Fill in the i-th digit
        a += _a[i] * 10**(308-i)
        s += _s[i] * 10**(308-i)
        b  = (s - a) % 10**(308-i+1)
        d  = (a - b) % 10**(308-i+1)
        
        # Fill in the (i-1)-th digit
        b += _b[i-1] * 10**(308-i+1)
        d += _d[i-1] * 10**(308-i+1)
        a  = (b + d) % 10**(308-i+2)
        s  = (a + b) % 10**(308-i+2)

    a += _a[0] * 10**308
    s += _s[0] * 10**308

    c = f = 0
    for i in range(308, 0, -2):
        # Fill in the i-th digit
        c += _c[i] * 10**(308-i)
        f  = (c - a) % 10**(308-i+1)

        # Fill in the (i-1)-th digit
        f += _f[i-1] * 10**(308-i+1)
        c  = (f + a) % 10**(308-i+2)
    
    c += _c[0] * 10**308
    f += _f[0] * 10**308

    # a = p^e mod n
    # b = q^e mod n

    # Sanity check
    assert int(str(a)[::2]) == s1
    assert int(str(b)[::2]) == s2
    assert int(str(s)[::2]) == s3
    assert int(str(d)[::2]) == s4
    assert a + b == s
    assert a - b == d
    assert c - a == f

    # a = p^65537 mod n
    # b = q^65537 mod n
    # c = 2^65537 * q^65537 mod n

    q = gcd(b, c)
    for k in range(2, 10**6):
        while q % k == 0:
            q //= k
    assert q.bit_length() == 513
    assert is_prime(q)
    
    dq = pow(e, -1, q-1)
    p = pow(a, dq, q) + q
    assert p.bit_length() == 513
    assert is_prime(p)

    n = p * q

    # Sanity check, the real one
    assert int(str(pow(p,     e, n))[::2]) == s1
    assert int(str(pow(q,     e, n))[::2]) == s2
    assert int(str(pow(p+q,   e, n))[::2]) == s3
    assert int(str(pow(p-q,   e, n))[::2]) == s4
    assert int(str(pow(2*q,   e, n))[::2]) == s5
    assert int(str(pow(2*q-p, e, n))[::2]) == s6

    phi = (p-1) * (q-1)
    d = pow(e, -1, phi)
    m0 = pow(c0, d, n)

    flag = int.to_bytes(m0, (m0.bit_length()+7)//8, 'big')
    print(f'{flag = }')

    return True

def main():
    id = 0
    while not attempt(id):
        id += 1

if __name__ == '__main__':
    main()


