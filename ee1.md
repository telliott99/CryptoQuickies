### Multiplicative inverse

(Note: every number here is an integer).

Suppose we know `e` and want to find `d` such that 

    e*d mod p = 1
    
If it's true that there exists such a number `d` then 

    e*d mod p = 1
    e*d mod p + np mod p = 1

for every `n`, because `n*p mod p = 0`, and so

    (e*d + n*p) mod p = 1

We will use this fact a bit later.

[link](http://www-math.ucdenver.edu/~wcherowi/courses/m5410/exeucalg.html)

#### Working through Euclid's theorem

Consider `gcd(81,57)`

```
81 = 1(57) + 24
57 = 2(24) +  9
24 = 2(9)  +  6
 9 = 1(6)  +  3
 6 = 2(3)  +  0
```

So `gcd(81,57) = 3`.

What we want to do next is to find integers (one negative) such that

```
p(a)  + s(b)  = 3
p(81) + s(57) = 3
```

Rearrange the next to last line (line no. 4) from the `gcd` calculation:

```
3 = 9 - 1(6)
```

Substitute for `6` from line no. 3 

```
 6 = 24 - 2(9)

 3 = 9 - 1[24 - 2(9)]
   = 3(9) - 1(24)
```

Substitute for `9` from line no. 2

``` 
 9 = 57 - 2(24)
 
 3 = 3[57 - 2(24)] - 1(24)
   = 3(57) - 7(24)
```

Finally, substitute for `24` from line no. 1

```
24 = 81 - 1(57)

3 = 3(57) - 7(24)
  = 3(57) - 7[81 - 1(57)]
  = 10(57) - 7(81)
  = -7(81) + 10(57)
```

And indeed, `-567 + 570 = 3`.

Thus, we've shown that

```
3 = p(a) + s(b)
```

where `p = -7` and `s = 10`.  

But if

```
3 = 10(57) - 7(81)
```

then what this means is that `10(57) = 3 mod 81`.

Paraphrasing the [link](http://www-math.ucdenver.edu/~wcherowi/courses/m5410/exeucalg.html):

"We want to do arithmetic modulo *n*, and in particular, for division we need to find the inverse of integers mod *n*. For large numbers, this turns out to be a difficult task (and not always possible).

It is known that a number *x* has an inverse mod *n* (i.e., a number *y* so that `xy = 1 mod n`) if and only if `gcd(x, n) = 1`."

Our example above had `gcd = 3`, but we are really interested in cases where `gcd = 1` because then we are guaranteed that an inverse exists.  

The simplest way to arrange this is to choose *n* prime, since then every integer less than *n* has `gcd = 1` with *n*.

The following simple Python function finds the inverse.  It is a "cleaned up" version of something I found on the web [here](https://www.johannes-bauer.com/compsci/ecc/).  

It is not so clear to me how it works.

``` python
def eea(a,b):
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
```

[eea.py](scripts/eea.orig.py)

I check the result from `eea` by using a brute-force approach to finding the inverse:

``` python
# requires a > b
def caveman(m,p):
    n = 2
    while m*n % p != 1:
        n += 1
    return n
```

and compare the results of the two functions like so:

```python
p = 127
for i in range(2,p):
    r = eea(p,i)
    if r < 0:  r += p
    print i, caveman(i,p), r
```

**output**

```
2 64 64
3 85 85
4 32 32
5 51 51
6 106 106
7 109 109
8 16 16
```

The two methods agree and we may also check by doing (for example)

    5 * 51 = 255,  127 * 2 = 254
    6 * 106 = 636, 127 * 5 = 635

For each pair we have that `p*r mod n = 1`.

To see how this function accomplishes what it does, we might print out the results for a particular simple, illustrative case.

#### Example 1

Again, we have this short function:

``` python
def eea(a,b):
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

print eea(81,57)
```

which prints the result `10`.  That's because

    57 * 10 % 81 = 3

and `3` is equal to `gcd(81,57)`.

which is the output from the Euclidean algorithm

Consider `gcd(81,57)`

```
81 = 1(57) + 24
57 = 2(24) +  9
24 = 2(9)  +  6
 9 = 1(6)  +  3
 6 = 2(3)  +  0
```

analyzed above.

But the requirement was that `eea(a,b)` only gives the modular multiplicative inverse provided that `gcd(a,b) = 1`.  So we really need a different example.

#### Example 2

If we know that `gcd(53,10) = 1` (because `53` is prime), and we do `eea(53,10)` and obtain `16`, we can check:

    10 * 16 = 160 = 53*3 + 1

We work through the Euclidean algorithm for `gcd(53,10)`:

```
53 = 5(10) + 3
10 = 3(3)  + 1
 3 = 3(1)  + 0
```

and so return `1`.

Let us do what we did before:

```
1 = 10 - 3(3)
```

since `3 = 53 - 5(10)`

```
1 = 10 - 3[53 - 5(10)]
1 = 16(10) - 3(53)
```

So we see that `16(10) mod 53 = 1`, by the argument above 

    ed mod p = 1
    ed mod p + np mod p = 1

for every `n` because `np mod p = 0` and so

    (ed + np) mod p = 1

Then the question is, how does `eea` come up with `16` from this process?  

The logic is

```
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
```

So if we start with:

```
a = 53;  b = 10
s = 1;   t = 0
u = 0;   v = 1
-----
q = 5;   r = 3
a = 10;  b = 3
s = 0 - (5 * 1) = -5
t = 1 - (5 * 0) = 1
u = 1;   v = 0
```

The second round is:

```
a = 10;  b =  3
s = -5;  t = 10
u =  1;  v =  0
-----
q = 3;   r = 1
a = 3;   b = 1
s = 1 - (3 * -5) =  16
t = 0 - (3 * 10) = -30
u = -5;  v = 10
```


The third round is:

```
a =  3;  b =   1
s = 16;  t = -30
u = -5;  v =  10
-----
q = 3
a = 1;  b = 0
s = -5 - (3 * 16) = -53
t = 10 - (3 * -30) = 100
u = 16;  v = -30
```

At the third round `b = 0` so we don't enter the loop.  We return `u = 16`.  

Even with all of this detailed output, it is difficult for me to see how it works.  For that reason I wrote my own version. [next](ee2.md).