### Euclidean algorithm

As a result of our interest in modular arithmetic, we take a look at the famous Euclidean algorithm, which yields the `gcd` (greatest common divisor) of two integers `a` and `b`.

It consists of the following steps:

* compute `r = a mod b`
* if `r == 0:  return b`
* set `a = b`
* set `b = r`

Example:

```
  a =   b * r +  m
421 = 111 x 3 + 88
111 =  88 x 1 + 23
 88 =  23 x 3 + 19
 23 =  19 x 1 +  4
 19 =   4 x 4 +  3
  4 =   3 x 1 +  1
  3 =   1 x 3 +  0
```

The last non-zero remainder is 1, which we return as `b` when `r = 0`.  This is `gcd(421,111).`  

`gcd = 1` means that these two numbers do not share any factors.  Hint:  421 is on this [list](https://primes.utm.edu/lists/small/1000.txt), although 111 is not.

Here are three very similar Python implementations.  We require `b < a` and if necessary we can do this before invoking the algorithmic code:

``` python
if b > a:
    a,b = b,a
```

My favorite loop `while True`:

``` python
def gcd(a,b):
    while True:
        r = a % b
        if r == 0:
            return b
        a,b = b,r

print gcd(421,111)  # 1
print gcd(60,24)    # 12
print gcd(11838*2888, 99991987*2888) # 2888
```

[code](scripts/gcd.py)

Although I like it, the `while True` irritates some people, who might prefer:

```python
def gcd(a,b):
    r = a % b
    while r != 0:
        a,b = b,r
        r = a % b
    return b
```

And here is a recursive version, which calls itself:

```python
def gcd(a,b):
    r = a % b
    if r == 0:
        return b
    return gcd(b,r)
```

#### Explanation

Consider two integers `a` and `b` and we compute `r = a mod b`.

One possibility is that `a` is evenly divided by `b`, then the result of the `mod` operation is zero, and `b` is the `gcd(a,b)`.

If not, then either `a` and `b` have at least one common divisor or they do not share a common factor (we do not consider `1` as a factor).

The mod operation can be expressed as
    
    r = a - nb

where `n` can be computed variously as the "floor" of `a/b` (the next smallest integer from the real number that is computed), or the integer `n` such that `nb < a` but `(n+1)b > a`.  (If there were an integer `n` so that `nb = a` exactly, that would correspond to the case of zero remainder).
    
So we suppose `a` and `b` have a common factor `f`.  Then we can factor `f` from each term of the previous equation:

    r = a - nb
    r = f(a/f - nb/f)

So, by the hypothesis of a common factor, the terms `a/f` and `nb/f` are integers.  But then clearly `r` is also evenly divided by `f` and

    r/f = a/f - nb/f

The insight is that now we can just find `gcd(b,m)`, since `b` and `m` also have the common factor `f`, and all the same logic applies.

It is easy to show that the algorithm always terminates, but I leave that aside for now.