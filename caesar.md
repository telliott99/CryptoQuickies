#### Caesar cipher

One of the earliest ciphers is the Caesar cipher, so named because Julius Caesar sometimes used it in his correspondence.

The idea is to switch every plaintext letter for a ciphertext letter that is advanced by 3 in alphabetical order.  

Thus

```
a -> D
b -> E
..
x -> A
y -> B
z -> C
```

(using lowercase for the *plaintext* and uppercase for the *ciphertext*).  At the end of the alphabet, it "wraps around" with `x -> A` and so on.

A simple implmentation is [here](caesar.py).

The output is

```
> python caesar.py
C3
abcdefghijklmnopqrstuvwxyz
DEFGHIJKLMNOPQRSTUVWXYZABC

rot13
abcdefghijklmnopqrstuvwxyz
NOPQRSTUVWXYZABCDEFGHIJKLM

and you too, brutus
DQG BRX WRR, EUXWXV
>
```

#### Multiplicative cipher

The idea of a multiplicative cipher is to take the index of each letter and multiply it by some fixed value like 3 (it is better to use a 1-based index).  The result (mod 26) is the index of the output from the uppercase alphabet.

```
> python mcipher.py 
1
abcdefghijklmnopqrstuvwxyz
BCDEFGHIJKLMNOPQRSTUVWXYZA

3
abcdefghijklmnopqrstuvwxyz
DGJMPSVYBEHKNQTWZCFILORUXA

5
abcdefghijklmnopqrstuvwxyz
FKPUZEJOTYDINSXCHMRWBGLQVA

...

25
abcdefghijklmnopqrstuvwxyz
ZYXWVUTSRQPONMLKJIHGFEDCBA

>
```

We check to see if the cipher is "good", that all 26 letters are possible outputs.  Math guys would say that these functions are bijective.  

We also look to see if the cipher is unique (if we can construct it using a smaller multiplicand, then it's not unique).

The good ones use every odd number in [1,25] except 13.  Odd numbers larger than 26 just repeat the previous results because

```
[(x + 26) * y] % 26 = [x * y] % 26
```

Neither 1 nor 25 are very interesting.  

Let's look at the code using 3 as multiplicand:

```
1 * 3 = 3
2 * 3 = 6
..
8 * 3 = 24
9 * 3 = 27 % 26 = 1
10 * 3 = 30 % 26 = 4
..
17 * 3 = 51 % 26 = 25
18 * 3 = 54 % 26 = 2
26 * 3 = 78 % 26 = 0
```

Even numbered multiplicands fail to make a good cipher because you never hit the odd outputs.

If you look at the script you'll see that I tried every value up to 1000.  In all, we found 12 values that make good ciphers.  It's not necessary to test any multiplicands `n > 26` because one of these has the same effect as `n % 26`.

It's interesting that the "bad" keys are the divisible by the prime factors of the alphabet size, 26.  Other alphabets, like Julius Caesar's Latin (21 characters) or Scandinavian languages (29 characters), would have different bad keys.




