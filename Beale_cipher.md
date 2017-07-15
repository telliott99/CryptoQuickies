#### More ciphers

Suppose we take as our "secret" text the Constitution of the United States.  This [file](scripts/constitution_preamble.txt) contains the first paragraph from this web [page](https://www.usconstitution.net/const.txt) following a bit of annotation.

This [script](scripts/we_the_people.py) gives us the first 256 characters in uppercase.

    WETHEPEOPLEOFTHEUNITEDSTATESINORDERTO
    ..
    ABLISHTHISCONSTITUTIONFORTHEUNITEDSTA

We could use this text as a one-time pad to encrypt a message like 

    ATTACKATDAWN

The encryption method is this:  for every character `m` of the message, take the corresponding character `k` from the pad (here I refer to it as the key).  `i` is the index of `m` offset by the index of `k`, mod `26`.  Return that character of the alphabet.

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

Then choose a row based on the key and the column based on the message character (or vice-versa).  Here is an nice [image](figs/vigenere.png).

This method is called the [Vigenère cipher](https://en.wikipedia.org/wiki/Vigenère_cipher).

In Python, I would do this with a dictionary of dictionaries:  `c = D[k[m]]`.

#### Transposition

The text we chose for our key is pretty famous.  We can try to obscure that by various manipulations.  One way is transposition.

Peter Norvig clued me to this elegant method of transposing a matrix ([here](http://norvig.com/python-iaq.html), about 2/3 of the way down the page):

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

Variations on the above lead to the idea of using a static page on the web as the basis for a one-time pad.

What about DNA?  There are a lot genes in Genbank!  

Each single base is worth 4-bits (one for each base of the four bases). 

We can encode the bases as

    a = 00
    t = 10
    g = 01
    c = 11

That makes every dinucleotide sequence equivalent to a hexadecimal base.

```
aa = 0000, ag = 0001, at = 0010, ac = 0011
ga = 0100, gg = 0101, gt = 0110, gc = 0111
ta = 1000, tg = 1001, tt = 1010, tc = 1011
ca = 1100, cg = 1101, ct = 1110, cc = 1111
```

So a 12-mer sequence like

    atgaccctttta
    
would be encoded in hex as

    24 fc a8

    
There is going to be some wastage going to a 26-character alphabet.  Thirteen would be a sequence like:

    a t g a c c c t t t t a g
    00100100111111101010100001

Make a binary code for the uppercase letters:

``` python
>>> def f(c):
...     n = ord(c) - ord('A')
...     return bin(n)[2:].zfill(5)
...
>>>
```
    
The first five letters of the Constitution are:

    W    E    T    H    E
    1011000100100110011100100

Now just XOR the two bit streams, padding the text with `0`:

    10110001001001100111001000
    00100100111111101010100001
    10010101110110001101101001
    
We can transmit that as hex.

``` python
>>> hex(int('10010101110110001101101000',2))
'0x2576368'
>>>
```

5 text characters turned into 26 binary digits, turned into 7 octal hex letters.  We waste a bit of keystream, but not that much.

We could use transposition as above to scramble the key a bit.  Or a spiral pattern.  Or seed a PNRG and choose the DNA letters according to that schedule.  But if you're going to do that, you might as well just use aes-cbc-128.

The secret key would just be the gene for that message. Or a genome and a position where to begin, and a direction.


