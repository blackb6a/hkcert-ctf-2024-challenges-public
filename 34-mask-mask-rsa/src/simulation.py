from Crypto.Util.number import getPrime, bytes_to_long


if __name__ == '__main__':
    good = count = 0
    while count <= 100000:
        if count > 0:
            print(f'{good/count*100:9.5f}% | {good}/{count}')

        count += 1

        e = 65537
        p, q = 1, 1
        while p == q:
            while (p-1) % e == 0:
                p = getPrime(513)
            while (q-1) % e == 0:
                q = getPrime(513)

        n = p * q
        # p > q

        a = pow(p, e, n)
        b = pow(q, e, n)
        
        if a < b:
            a, b = b, a
            p, q = q, p

        c = pow(2*q, e, n)

        if not (10**308 <= a < 10**309): continue
        if not (10**307 <= b < 10**308): continue

        if a + b >= n: continue
        if not (10**307 <= a-b < 10**308): continue

        if not (10**308 <= c < 10**309): continue
        if not (10**307 <= c-a < 10**308): continue


        good += 1

# 100,000 pairs of (p, q) are executed and 1,860 matches the condition. The hit rate is around 1 in 54.
