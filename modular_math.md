### Modular arithmetic

[link](https://www.johannes-bauer.com/compsci/ecc/#anchor13)

We want to do arithmetic `mod` some prime number `p`, where the numbers can be much larger than the largest unsigned integer on the machine:  `2**64`.

[code](scripts/modular.py)

#### Addition

According to the reference, we just add `i` and `j` together, and then if the result `r > p`, subtract `p`.  This assumes that `i < p` and `j < p`.

``` python
def add_mod(i,j,p=p):
    if i >= p or j >= p:
        raise ValueError
    r = i + j
    if r >= p:
        r -= p
    return r
```

#### Subtraction

This is can be handled the same way, except that if the result is less than zero, we add back `p`.

``` python
def subtract_mod(i,j,p=p):
    if i >= p or j >= p:
        raise ValueError
    r = i - j
    if r < 0:
        r += p
    return r
```

#### Multiplication

Here is where it gets interesting.  Consider `i` times `j`.  

We should start by choosing the factor which has fewest `1`s in its binary representation.

``` python
def test_digits(i,j):
    left = bin(i)[2:].count('1')
    return left >= bin(j)[2:].count('1')
```

`n` is initialized with the value of `i`.

We test the digits of `j` by a combination of right-shift and binary AND.  First do `j & 1`.  If the result is `1` we add the current value of `n` to `r`, which accumulates the result.

At the same time, each round we do a right-shift of 1 bit for `j`, and also double the value of `n`.

``` python
def multiply_mod(i,j,p):
    if test_digits(i,j):
       i,j = j,i
    n = i
    r = 0
    while j > 0:
        if j & 1:
            r = r + n
            while r >= p:
                r -= p
        # prepare for next round
        j = j >> 1  # right shift j
        n = n + n   # double n
        while n >= p:
            n -= p
    return r
```

#### Division

We handle division using the multiplicative inverse.  If we're doing arithmetic mod a prime number, then it's guaranteed that every number has an inverse such that

    n * n_inv = 1

``` python
def eea(i, j):
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

print eea(7,121)                # (1, -3, 52)
print multiply_mod(7,52,121)    # 1
print eea(52,121)               # 7
```

Let's put off an analysis of this for another time.

#### Exponentiation

We use essentially the same setup as for multiplication.  Except we multiply rather than add.

``` python
def exponentiate_mod(i,j,p):
    if test_digits(i,j):
       i,j = j,i
    n = i
    r = 1
    while j > 0:
        if j & 1:
            r = multiply_mod(r,n,p)
            while r >= p:
                r -= p
        # prepare for next round
        j = j >> 1              # right shift j
        n = multiply_mod(n,n,p)   # square n
        while n >= p:
            n -= p
    return r

def test4():
    print exponentiate_mod(13,57,101)
    print exponentiate_mod(2,40,101)
    print exponentiate_mod(314159265359,271828182846,2**127-1)

test4()
```

The result of that last calculation is 

    122574892404968648570787373191368149806

which matches my source.