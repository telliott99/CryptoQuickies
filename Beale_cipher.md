#### More ciphers

Suppose we take as our "secret" text the Constitution of the United States.  This [file](scripts/constitution_preamble.txt) contains the first paragraph from this web [page](https://www.usconstitution.net/const.txt) with a bit of annotation removed.

This [script](scripts/we_the_people.py) yields the first 256 characters in uppercase.

    WETHEPEOPLEOFTHEUNITEDSTATESINORDERTO
    ..
    ABLISHTHISCONSTITUTIONFORTHEUNITEDSTA

We could use the text as a one-time pad to encrypt a message like 

    ATTACKATDAWN

The encryption method is this:  for every character `m` of the message, take the corresponding character `k` from the pad (here I refer to it as the key).  `i` is the index of `m` plus the index of `k`, mod `26`.  Return that character of the alphabet.

``` python
def f(m, k, mode='enc'):
    n = len(alpha)
    i = alpha.index(m)
    j = alpha.index(k)
    if mode == 'enc':
        i += j
        i %= n
    elif mode == 'dec':
        i -= j
        if i < 0:
            i += n
    else:
        raise ModeError
    return alpha[i]
```

**output**

```
> python we_the_people.py 
ATTACKATDAWN
WETHEPEOPLEO
WXMHGZEHSLAB
ATTACKATDAWN
>
```

Rather than do the calculation for each character, another method is to construct a table such as this:

```
[ABCDEFGHIJKLMNOPQRSTUVWXYZ,
 BCDEFGHIJKLMNOPQRSTUVWXYZA,
 CDEFGHIJKLMNOPQRSTUVWXYZAB,
...
 YZABCDEFGHIJKLMNOPQRSTUVWX,
 ZABCDEFGHIJKLMNOPQRSTUVWXY]
```

Then choose a row based on the key and the column based on the message character (or vice-versa).  Here is a nice [image](figs/vigenere.png).

This method is called the [Vigenère cipher](https://en.wikipedia.org/wiki/Vigenère_cipher).

Here is Python code to do this with a list:

```python
>>> alpha = 'ABCDE'
>>> n = len(alpha) + 1
>>> s = alpha * n
>>> L = list()
>>> for i in range(0,len(s),n):
...     L.append(s[i:i+n-1])
... 
>>> print '\n'.join(L)
ABCDE
BCDEA
CDEAB
DEABC
EABCD
>>>
```

I might do this with a dictionary of dictionaries:  `c = D[k[m]]`.

```python
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
n = len(alpha)
s = alpha*2
D = dict()

for i,k in enumerate(alpha):
    sD = dict(zip(alpha,s[i:i+n]))
    D[k] = sD

#---------------------

msg = 'ATTACKATDAWN'
key = 'WETHEPEOPLEO'

pL = list()
for m,k in zip(msg,key):
    pL.append(D[k][m])
print ''.join(pL)    # WXMHGZEHSLAB
```

#### Transposition

The text we chose for our key is pretty famous.  We can try to obscure that by various manipulations.  One way is transposition.

Peter Norvig's notes about Python showed me this elegant method of transposing a matrix ([here](http://norvig.com/python-iaq.html), about 2/3 of the way down the page):

    def transpose(L):
        return zip(*L)

I used that to transpose our text:

    WUDRIDICMLERDRHN
    ENEFSOTOOFBTODTF
    TIREHMYMTALYUAHO
    HTTCJEPMERETRIIR
    EEOTUSROTESOPNST
    PDFUSTONHASOOACH
    ESONTIVDENIUSNOE
    OTRIICIEGDNRTDNU
    PAMOCTDFESGSEESN
    LTANEREENESERSTI
    EEMEIAFNECOLITIT
    OSOSNNOCRUFVTATE
    FIRTSQREARLEYBUD
    TNEAUUTPLEISDLTS
    HOPBRIHRWTBAOIIT
    ERELELEOEHENOSOA

Read down the columns to recover the text we started with.

#### DNA sequence

The above example suggests the idea of using a static page on the web as the basis for a one-time pad.

What about DNA?  There are a lot genes in Genbank!  

Each single base is worth 4-bits (one for each base of the four bases). 

We can encode the bases as

    a = 00
    t = 10
    g = 01
    c = 11

That makes every dinucleotide sequence equivalent to a hexadecimal base.

```
aa = 0000 = 0, ag = 0001 = 1, 
at = 0010 = 2, ac = 0011 = 3
ga = 0100 = 4, gg = 0101 = 5, 
gt = 0110 = 6, gc = 0111 = 7
ta = 1000 = 8, tg = 1001 = 9, 
tt = 1010 = a, tc = 1011 = b,
ca = 1100 = c, cg = 1101 = d, 
ct = 1110 = e, cc = 1111 = f
```

So a 12-mer sequence like

    atgaccctttta
    
would be encoded in hex as

    0x24fea8

    
There will be some wastage going to a 26-character alphabet.  Thirteen nucleotides would be a sequence like:

    a t g a c c c t t t t a g
    00100100111111101010100001

Construct a binary code for the uppercase letters:

``` python
>>> def f(c):
...     n = ord(c) - ord('A')
...     return bin(n)[2:].zfill(5)
...
>>>
```
    
The first five letters of the Constitution are:

    W     E     T     H     E
    10110 00100 10011 00111 00100

Now just XOR the two bit streams, padding the text with `0`:

    10110001001001100111001000
    00100100111111101010100001
    10010101110110001101101001
    
We can transmit that as hex.

    0x95d8da..


5 text characters turned into 26 binary digits, turned into 6 1/2 octal hex letters.  We waste a bit of keystream, but not that much.

We could use transposition as above to scramble the key a bit.  Or a spiral pattern.  Or seed a PNRG and choose the DNA letters according to that schedule.  But if you're going to do that, you might as well just use aes-cbc-128.

The secret key would just be the gene for that message. Or a genome and a position where to begin, and a direction.


