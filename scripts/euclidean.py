
# requires a > b
def gcd(a,b):
    m = a % b
    while not m == 0:
        a,b = b,m
        m = a % b
    return b

def test_gcd():
    print gcd(421,111)  # 1
    print gcd(60,24)    # 12
    print gcd(11838*2888, 99991987*2888) # 2888

# test_gcd()

# requires a > b
def caveman(m,p):
    n = 2
    while m*n % p != 1:
        n += 1
    return n

def test_caveman():
    print caveman(1234, 2003)  # 112
    print caveman(112, 2003)   # 1234

# test_caveman()

def eea(i, j):
    if j > i:
        i,j = j,i
    assert(isinstance(i, int))
    assert(isinstance(j, int))
    (s, t, u, v) = (1, 0, 0, 1)
    while j != 0:
        (q, r) = (i // j, i % j)
        (unew, vnew) = (s, t)
        s = u - (q * s)
        t = v - (q * t)
        (i, j) = (j, r)
        (u, v) = (unew, vnew)
    (d, m, n) = (i, u, v)
    return (d, m, n)

# requires a > b
def my_eea(a,b):
    s, t = 1, 0
    u, v = 0, 1
    while b != 0:
        q = a / b
        a, b = b, a % b
        
        tmp = s, t
        s = u - (q * s)
        t = v - (q * t)
        (u,v) = tmp
    return u


p = 127
for i in range(2,p):
    r = my_eea(p,i)
    if r < 0:  r += p
    print i, caveman(i,p), r




