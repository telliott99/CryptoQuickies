<script type="text/javascript" async 
src="/Users/telliott_admin/MathJax/MathJax.js?
config=TeX-MML-AM_CHTML"></script>

### Fermat's Theorem

If `p` is prime and `0 < a < p` then

<tt>a<sup>p-1</sup> mod p = 1</tt>

Consider `p = 7`:

``` python
1**6       1 % 7 = 1
2**6 =    64 % 7 = 1
3**6 =   729 % 7 = 1
4**6 =  4096 % 7 = 1
5**6 = 15625 % 7 = 1
6**6 = 46656 % 7 = 1
```

[Here](figs/Fermat13.png) is a table from Laws of Cryptography  [pdf](http://www.cs.utsa.edu/~wagner/lawsbookcolor/laws.pdf) for `p = 13`, which computes such powers more efficiently.

Let's do the calculation for `a = 7, p = 13`:

```
7**1  =       7
7**2  = 49 = 10
7**3  = 70 =  5
7**4  = 35 =  9
7**5  = 63 = 11
7**6  = 77 = 12
7**7  = 84 =  6
7**8  = 42 =  3
7**9  = 21 =  8
7**10 = 56 =  4
7**11 = 28 =  2
7**12 = 14 =  1
```

So, indeed, as the theorem says, we come around to <tt>7<sup>12</sup> mod 13 = 1</tt>.

The number `7` is called a generator because its powers generate all the values in the field Z<sub>13</sub>. `2, 6` and `11` are also generators for this field.

Other values have shorter repeats.  For example:

```
12**1 =       12
12**2 = 144 =  1
12**3 =       12
```

We just repeat `12 1 12 1 ...` for six cycles.  There are other curious patterns:  for example `9` gives `9 3 1` while `3` gives `3 9 1`, which I guess makes sense.  `4` gives `4 3 9 12 10 1` while `10` gives `10 12 9 3 4`, the reverse.  The lengths of these runs are divisors of 12.

As the source says:  "Because a  to a power x mod p always starts repeating after the power reaches p-1, one can reduce the power mod p-1      and still get the same answer. 

Thus no matter how big the power might be

<tt>a<sup>x</sup> mod p = a<sup>x mod p-1</sup> mod p</tt>

For example, `mod 13`:

<tt>a<sup>29</sup> = a<sup>29 mod 12</sup> = a<sup>5</sup></tt>

#### Euler's Theorem

This one looks pretty similar to what we've been talking about.

**Fermat**

$$a^{p-1} \text{ mod } p = 1$$

**Euler**

$$a^{\phi-1} \text{ mod } \phi = 1$$

where &phi; is defined as

$$\phi(n) = n \ \Pi \ (1 - \frac{1}{p_i})$$

and p<sub>i</sub> are the prime factors of *n*.  If *n* were prime we would have

```
n(1- 1/n) = (n-1)
```

In the case of RSA primes where `n = pq` we get

```
pq(1 -1/p)(1 - 1/q) = (p-1)(q-1)
```

[Here](figs/EulerTotient.png) is what that looks like.

