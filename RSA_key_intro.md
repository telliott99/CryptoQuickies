#### Public key structure

RSA keys are some multiple of 1024 bits, such as 1024, 2048, or 4096 bits.

It will make it easier to examine the structure of a key if we use a short one.  

The Python [rsa](https://pypi.python.org/pypi/rsa) module allows that.

```
> pip install rsa
...
>>> import rsa
>>> p = 409
>>> q = 211
>>> n = p*q
>>> n
86299
>>> e = 17
>>> 
```
We have our numbers, let's make a public key.

```
>>> pub_key = rsa.PublicKey(n=n,e=e)
>>> s = pub_key.save_pkcs1()
>>> print s
-----BEGIN RSA PUBLIC KEY-----
MAgCAwFRGwIBEQ==
-----END RSA PUBLIC KEY-----
```

This line

    -----BEGIN RSA PUBLIC KEY-----

identifies the format as PKCS #1.

```
>>> from base64 import b64decode as dec
>>> s = dec('MAgCAwFRGwIBEQ==')
'0\x08\x02\x03\x01Q\x1b\x02\x01\x11'
>>> L = [ord(c) for c in s]
>>> L
[48, 8, 2, 3, 1, 81, 27, 2, 1, 17]
>>>
```
Our super-duper public key consists of a grand total of 10 bytes.

The first thing we recognize is that the very last byte holds the value of `e`.

A small calculation shows that the three bytes `1,81,27` hold the value of `n` because

```
>>> 1 * 256**2 + 81 * 256 + 27
86299
>>>
```

We might also have done this:

```
>>> s = '0\x08\x02\x03\x01Q\x1b\x02\x01\x11'
>>> import binascii
>>> binascii.hexlify(s)
'3008020301511b020111'
```

Pick out the correct bytes (5-7):

```
>>> int('01511b',16)
86299
>>>
```

The `3` preceeding these bytes and the `1` preceeding `17` each presumably refers to the length of the data section for that value.

The key can be saved in different formats:  this one is `PKCS#1`.  

And another very common format is `SSH`.  All this makes life challenging.

According to [this](http://blog.oddbit.com/2011/05/08/converting-openssh-public-keys/)

    The data in a PKCS#1 key is encoded using DER, which is a set of rules for serializing ASN.1 data

I haven't looked to much into this but I know that PEM is the base64-encoded version of DER binary data.

Looking at our data
    
    48, 8, 2, 3, 1, 81, 27, 2, 1, 17

I wonder if the `2` is just some kind of spacer, and the `48 8` is perhaps a header.

Let's try another example.  Go back to the keys we computed in the math [write-up](public-key math.md):


	p = 961748941
	q = 982451653
	n = p*q = 944871836856449473
	e = 65537
	phi = 944871834912248880
	d = 8578341116816273

Now use the rsa module:

```
>>> import rsa
>>> n = 944871836856449473
>>> e = 65537
>>> pub_key = rsa.PublicKey(n=n,e=e)
>>> s = pub_key.save_pkcs1()
>>> print s
-----BEGIN RSA PUBLIC KEY-----
MA8CCA0c2+3yGXnBAgMBAAE=
-----END RSA PUBLIC KEY-----

>>> from base64 import b64decode as dec
>>> s = dec('MA8CCA0c2+3yGXnBAgMBAAE=')
>>> L = [ord(c) for c in s]
>>> L
[48, 15, 2, 8, 13, 28, 219, 237, 242, 25, 121, 193, 2, 3, 1, 0, 1]
>>>
```

Write the output on two lines:

    [48, 15, 2, 8, 13, 28, 219, 237, 
    242, 25, 121, 193, 2, 3, 1, 0, 1]

Comparing with our previous effort

    48, 8, 2, 3, 1, 81, 27, 2, 1, 17

The last four bytes are now

    3, 1, 0, 1

This is clearly the length of this section of the data plus `1 * 256**2 + 1 = 65537`.

Assuming `2` is a separator, we have for the previous section `8` as the length plus:

    13, 28, 219, 237, 242, 25, 121, 193

`n` is relatively large

    n = p*q = 944871836856449473

Let's try it

```
>>> m = 0
>>> L = [13, 28, 219, 237, 242, 25, 121, 193]
>>> for i,n in enumerate(L):
...     m += 256**(7-i)*n
... 
>>> 
>>> m
944871836856449473
>>>
```

Alternatively

```
>>> from base64 import b64decode as dec
>>> s = dec('MA8CCA0c2+3yGXnBAgMBAAE=')
>>> t = s[4:12]
>>> import binascii
>>> h = binascii.hexlify(t)
>>> h
'0d1cdbedf21979c1'
>>> int(h,16)
944871836856449473
>>>
```

Again

    n = p*q = 944871836856449473

So that's a match.

Going back to 

    [48, 15, 2, 8, 13, 28, 219, 237, 
    242, 25, 121, 193, 2, 3, 1, 0, 1]

We've explained everything except for the fact that in the first example we had `8` as the second byte and here we have `15`.  This is consistent with the second byte being the overall length of everything that follows.

#### Private key structure

	p = 961748941
	q = 982451653
	n = p*q = 944871836856449473
	e = 65537
	phi = 944871834912248880
	d = 8578341116816273

I did this in a [script](parse.py), using the methods we just discussed.  The output is

```
> python parse.py 
-----BEGIN RSA PRIVATE KEY-----
MDkCAQACCA0c2+3yGXnBAgMBAAECBx559K8Hq5ECBDlTH80CBDqPBcUCBBEqrXkC
BCc4mh0CBACAc5Q=
-----END RSA PRIVATE KEY-----

MDkCAQACCA0c2+3yGXnBAgMBAAECBx559K8Hq5ECBDlTH80C\
BDqPBcUCBBEqrXkCBCc4mh0CBACAc5Q=
944871836856449473   0d1cdbedf21979c1 n
             65537             010001 e
  8578341116816273     1e79f4af07ab91 d
         961748941           39531fcd p
         982451653           3a8f05c5 q
         288009593           112aad79
         658020893           27389a1d
           8418196           00807394
>
```

These are exactly in the order that we specified them to the constructor.

We have three extra values

    288009593
    658020893
    8418196

According to [this](https://tools.ietf.org/html/rfc3447#page-44), these fields are:  

* d mod (p-1)
* d mod (q-1)
* (inverse of q) mod p

```
>>> d % (p-1)
288009593
>>> d % (q-1)
658020893
>>> 8418196 * q % p
1
>>>
```

That's a match! 