#### Public key structure

RSA keys are some multiple of 1024 bits, like 1024, 2048, 4096 bits.

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
We have our numbers, let's make a key.

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

identifies the format as PKCS#1.

```
>>> from base64 import b64decode as dec
>>> s = dec('MAgCAwFRGwIBEQ==')
'0\x08\x02\x03\x01Q\x1b\x02\x01\x11'
>>> L = [ord(c) for c in s]
>>> L
[48, 8, 2, 3, 1, 81, 27, 2, 1, 17]
>>>
```
So we have a grand total of 10 bytes in our super-duper public key.

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

The `3` preceeding these bytes and the `1` preceeding `17` presumably refer to the length of the data section for each value.

The key can be saved in different formats:  this one is `PKCS#1`.  The other one that the rsa module uses is `PKCS#1.5` PEM-encoding.  

And another very common format is `SSH`.  All this makes life challenging.

According to [this](http://blog.oddbit.com/2011/05/08/converting-openssh-public-keys/)

    The data in a PKCS#1 key is encoded using DER, which is a set of rules for serializing ASN.1 data

I haven't looked to much into this.

From our data
    
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

```
>>> 
>>> priv_key = rsa.PrivateKey(n,e,d,p,q)
>>> print priv_key
PrivateKey(944871836856449473, 65537, 8578341116816273, 961748941, 982451653)
>>> s = priv_key.save_pkcs1()
>>> print s
-----BEGIN RSA PRIVATE KEY-----
MDkCAQACCA0c2+3yGXnBAgMBAAECBx559K8Hq5ECBDlTH80CBDqPBcUCBBEqrXkC
BCc4mh0CBACAc5Q=
-----END RSA PRIVATE KEY-----
>>> s = dec('MDkCAQACCA0c2+3yGXnBAgMBAAECBx559K8Hq5ECBDlTH80CBDqPBcUCBBEqrXkCBCc4mh0CBACAc5Q=')
>>> L = [ord(c) for c in s]
>>> len(L)
59
>>> 
```

It's probably easier in hex

```
>>> binascii.hexlify(s)
'303902010002080d1cdbedf21979c1020301000102071e79f4af07ab91020439531fcd02043a8f05c50204112aad79020427389a1d020400807394'
>>>
```

Break it up by splitting on `02`

    3039
    020100
    02080d1cdbedf21979c1
    0203010001
    02071e79f4af07ab91
    020439531fcd
    02043a8f05c5
    0204112aad79
    020427389a1d
    020400807394
    

```
>>> int('0d1cdbedf21979c1',16)
944871836856449473
>>>
```

Recall:

	p = 961748941
	q = 982451653
	n = p*q = 944871836856449473
	e = 65537
	phi = 944871834912248880
	d = 8578341116816273


So the first long value is *n*. The next is clearly *e*.  Then we have

```
>>> int('1e79f4af07ab91',16)
8578341116816273
>>> 
```

That would be *d*.  Then *p*

```
>>> int('39531fcd',16)
961748941
>>> p
961748941
```

followed by *q*

```
>>> int('3a8f05c5',16)
982451653
>>> q
982451653
>>>
```

Exactly in the order that we specified them to the constructor.

We have three more values

```
>>> int('112aad79',16)
288009593
>>> int('27389a1d',16)
658020893
>>> int('00807394',16)
8418196
>>>
```

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