### Coding the extended Euclidean algorithm

I found a nice page about this topic 
[link](http://www-math.ucdenver.edu/~wcherowi/courses/m5410/exeucalg.html)

The extended Euclidean algorithm uses information that is generated in the Euclidean algorithm, which is normally discarded, in order to compute multiplicative inverses in modular arithmetic.

#### Example

The easiest way to understand this is by example.  Suppose we compute `gcd(60,13)`.

```
60 = 4 x 13 + 8
13 = 1 x  8 + 5
 8 = 1 x  5 + 3
 5 = 1 x  3 + 2
 3 = 1 x  2 + 1
 2 = 2 x  1 + 0
```

At this point `b == 1` and `r == 0`, so the result is equal to `1`.

There is additional information here, both in the quotients `q` in `a = qb + r`, and in the remainders.  Let's focus on the `q` values.

What we do first is discard the last row, and then also rearrange each item to be in the form `r = a - q(b)`:

```
 8 = 60 - 4(13)
 5 = 13 - 1(8)
 3 =  8 - 1(5)
 2 =  5 - 1(3)
 1 =  3 - 1(2)
```

Process the items in inverse order.

    1 =  3 - 1(2)

Now, substitute for `2` from the line above:

    1 = 3 -  1[5 - 1(3)]

We have `-1(5)` and then two factors containing `(3)`:

    1 = -1(5) + (1 + 1)(3)
      = -1(5) + 2(3)

And we can check easily that this is correct.  Continue with round 3:

    1 = -1(5) + 2(3)
    1 = -1(5) + 2[8 - 1(5)]
      =  2(8) - 3(5)
 
At each stage we generate a true equality, we always have the larger number with two terms to be combined.  And the signs stay with the terms:  all terms with `(5)` will be negative, for example.

Round 4:

    1 = 2(8) - 3(5)
      = 2(8) - 3[13 - 1(8)]
      = -3(13) + 5(8)

Round 5:

    1 = -3(13) + 5(8)
      = -3(13) + 5[60 - 4(13)]
      = -23(13) + 5(60)

Check that `23(13) = 299`.  Yes.

You remember from [last time](ee1.md) when we said that we can take an equation like

     1 = -23(13) + 5(60)

and take the `mod` of both sides and even of the individual terms

     1 mod 60 = -23(13) mod 60 + 5(60) mod 60

But the left-hand side is just `1` and the last term is `0` so we have

     1 = -23(13) mod 60

The very definition of the modular multiplicative inverse!  The only other step is to realize that `-23 mod 60 = 37`, and indeed

    37 * 13 % 60 = 1
    
#### Code

Code was a bit challenging.  I couldn't really understand the code I got from the web.  I tried doing things symbolically, but it turned into a mess.  I deleted it, but it had terms like

    q1q3 + q1q5 + q1q2q3q4q5 + ...
    
But after staring at the example for a while, I was able to come up with code which returns all the data from `gcd` (we need only the quotients but the rest of it makes it easy to print exactly what we have above.

Using those quotients and starting with the right `a` and `b`, the loop for rounds 2 and after is

``` python
for i in range(2,N):
    a,b,q,r = L.pop(0)
    tmp = ca
    ca = cb
    cb = tmp - q * cb
    t = a,b,q,r,ca,cb
    pp(t)   # pretty print
```

which is simple enough that you have to wonder why I've struggled with this all day.

The heart of it is to have two variables which hold the values of the coefficients of `a` and `b`:  `ca` and `cb`.  The value of `cb` is used in updating `ca` and vice-versa, so we use `tmp` to cache the value of `ca` for a second.

Anyway, the script [eea.py](scripts/eea.py) takes two integers on the command line and generates 

```
> python eea.py 60 13
a=3,b=2,q=1,r=1,ca=1,cb=-1
a=5,b=3,q=1,r=2,ca=-1,cb=2
a=8,b=5,q=1,r=3,ca=2,cb=-3
a=13,b=8,q=1,r=5,ca=-3,cb=5
a=60,b=13,q=4,r=8,ca=5,cb=-23
multiplicative inverse of 13 is 37 mod 60
>
```

which I think you will find matches what we had above.

Just picking two random numbers out of thin air

```
> python eea.py 333337 58498
a=16,b=3,q=5,r=1,ca=1,cb=-5
a=35,b=16,q=2,r=3,ca=-5,cb=11
a=86,b=35,q=2,r=16,ca=11,cb=-27
a=465,b=86,q=5,r=35,ca=-27,cb=146
a=1016,b=465,q=2,r=86,ca=146,cb=-319
a=5545,b=1016,q=5,r=465,ca=-319,cb=1741
a=17651,b=5545,q=3,r=1016,ca=1741,cb=-5542
a=40847,b=17651,q=2,r=5545,ca=-5542,cb=12825
a=58498,b=40847,q=1,r=17651,ca=12825,cb=-18367
a=333337,b=58498,q=5,r=40847,ca=-18367,cb=104660
multiplicative inverse of 58498 is 104660 mod 333337
>
```
Note that the first row has `r=1` (these two are coprime).

And just to check:

```
>>> 58498*104660 % 333337
1
>>>
```
