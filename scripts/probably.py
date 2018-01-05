from random import choice as ch

def doOne():
    while True:
        digits = '0123456789'
        a = ch(digits[1:])
        b = ''.join([ch(digits) for i in range(98)])
        c = ch('1379')
        p = int(a+b+c)
        if p % 3 == 0:
            continue
        if pow(3,p-1,p) == 1:
            break
    return p

p = doOne()
q = doOne()
n = p*q
phi = (p-1)*(q-1)
e = 65537


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("modular inverse does not exist")
    else:
        return x % m

d = egcd(phi,e)[2]

m = doOne()
c = pow(m,e,n)
p = pow(c,d,n)

print m
print p