#### Analyzing ssh-keygen public format

We obtained a pair of 1024-bit RSA keys from `ssh-keygen` by

    ssh-keygen -b 1024 -t rsa -f kf -N ''

The public key file `kf.pub` starts with

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQD1AEKcLXe9iER6H..
user@computer_name
```

Copy-paste the base64 part into `data.txt` and load the data into Python (or just paste it into the interpreter using a triple-quoted string)

    fn = 'data.txt'
    fh = open(fn)
    data = fh.read()
    fh.close()
    from base64 import b64decode as dec
    s = dec(data)
    s

We see

```python
>>> fn = 'data.txt'
>>> fh = open(fn)
>>> data = fh.read()
>>> fh.close()
>>> from base64 import b64decode as dec
>>> s = dec(data)
>>> s
'\x00\x00\x00\x07ssh-rsa\x00\x00\x00\x03..
>>> L = [ord(c) for c in s]
>>> L = L[21:]
>>> L1 = L[:20]
>>> L1
[0, 0, 0, 7, 115, 115, 104, 45, 114, 115, 97, 0, 0, 0, 3, 1, 0, 1, 0, 0]
>>> L
[129, 0, 245, 0, 66, 156, 45, 119, 189, 136, 68, 122, 30, 171, 61, 97, 220...
>>> L.pop(0)
129
>>> len(L)
129
```

As described in my blog [post](http://telliott99.blogspot.com/2011/08/dissecting-rsa-keys-in-python-2.html)

The base64-encoded key data consists of a big-endian UInt64 with the value 7, which indicates the length of that section followed by the data:  `ssh-rsa`.

Next is a length 3 followed by 1, 0, 1.  The 1,0,1 is 1 * 256**2 + 1 = 65537.

Then finally we have a length of 129, followed by 129 bytes.


```python
>>> hL = [hex(n)[2:].zfill(2) for n in L]
>>> eval('0x' + ''.join(hL))
17204556452999033524595293865438703347941170
...
0578871752450829431753153653389483L
>>>
```

That should be n.  Is there a way to check it?  Sure!

There is an `openssl` tool to extract `e` and `n` from a public key that is in standard PKCS #1 PEM format.  

We first need to convert to that format (see [here](RSA_key_formats.md)).

```
> ssh-keygen -e -m pkcs8 -f kf.pub > kf2.pub
> openssl rsa -pubin -inform PEM -text -noout < kf2.pub
Modulus (1024 bit):
    00:f5:00:42:9c:2d:77:bd:88:44:7a:1e:ab:3d:61:
    dc:f0:74:c5:89:98:40:e3:8b:5d:96:34:e1:c3:90:
    1b:ef:4c:af:44:e1:89:c0:31:c8:eb:8b:26:e2:1c:
    83:43:40:2f:e2:72:c0:a5:23:d1:7a:b7:a5:b4:ba:
    4f:93:07:a3:83:d5:b2:57:f9:2a:76:81:d0:0e:9a:
    a1:15:da:05:7e:15:af:4b:77:29:fa:b0:31:0f:10:
    fd:74:9c:ca:df:a6:14:99:af:a0:a6:0a:b4:cf:4c:
    09:b9:13:76:5b:89:a1:99:29:34:be:17:5d:c0:16:
    6a:e5:cb:4d:ad:d6:3e:38:ab
Exponent: 65537 (0x10001)
>
```

Paste that hex into the interpreter and do:

```python
>>> s = ''.join(s.strip().split())
>>> s = s.replace(':','')
>>> eval('0x' + s)
17204556452999033524595293865438703347941170
...
0578871752450829431753153653389483L
>>>
```
That's a match!

#### ssh-keygen private key

To dissect a key of this type, we should first figure out the values so we have some idea of what to look for.  

Use the `rsa` module to do that:

```python
>>> import rsa
>>> fn = 'kf'
>>> fh = open(fn)
>>> data = fh.read()
>>> fh.close()
>>> data
'-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQD1AEKcLXe9iER6Hqs9YdzwdMWJmEDji12...
>>> privk = rsa.PrivateKey.load_pkcs1(data)
>>> privk.n
17204556452999033524595293865438703347941170
...
0578871752450829431753153653389483L
```

I will print the values in hex format, and break up the lines for readability. 

``` python
>>> hex(privk.n)
'0xf500429c2d77bd88447a1eab3d61dcf074c5899840e38b5d963\
4e1c3901bef4caf44e189c031c8eb8b26e21c8343402fe272c0a52\
3d17ab7a5b4ba4f9307a383d5b257f92a7681d00e9aa115da057e1\
5af4b7729fab0310f10fd749ccadfa61499afa0a60ab4cf4c09b91\
3765b89a1992934be175dc0166ae5cb4dadd63e38abL'
>>> hex(privk.e)
'0x10001'
>>> hex(privk.p)
'0xffb4b12b9f8b57fc9cab6194c5e6cf96e9cd7a4c0250c161b66\
dac6f8e867c9d1b1670b186b1ceb21f51534ad3340e74287e55f0a\
50d8d396633be122854cc1fL'
>>> hex(privk.q)
'0xf5486a5ae2e2e81454220596be4864b218c7fb1e4158be9a485\
1a986a1960fd711b728a3e5b30dc454ef359e5ddda3c7657abfba8\
a2c1b2e570fe82cb25d41f5L'
>>> hex(privk.d)
'0x5dba6bc133e3cb2e8683f197b133ef424e6a03e9ab6961b7bbe\
f1f2fa1c20e1a583311d591217aac21e00e40ba36d027818a4508e\
85b0b87966d3d9993b62867577ffe501ed889ce83a82fafe686c45\
4f8fde84d5fc7bf967c3427a5b52f4e6e81393773301d85d91005b\
d7ba3f39e2f4163e15b01b18c04c94c9c51690a8681L'
>>>
```

To actually do the dissection, I wrote [script.py](script.py).  

First we print the hex and the integer value of the 4th element (1-based indexing).  

After stripping off the two leading bytes, which repeat the length (`129` or `0x81`), this value is clearly `n`.  Then print the hex for all the values in the key.

``` 
> python script.py 
n
00f500429c2d77bd8844 166ae5cb4dadd63e38ab
17204556452999033524 29431753153653389483
 1 3082
 2 5c
 3 0100
 4 818100f500429c2d77bd88447a1eab3d61dcf074
 5 03010001
 6 81805dba6bc133e3cb2e8683f197b133ef424e6a
 7 4100ffb4b12b9f8b57fc9cab6194c5e6cf96e9cd
 8 50c161b66dac6f8e867c9d1b1670b186b1ceb21f
 9 4100f5486a5ae2e2e81454220596be4864b218c7
10 40641d1fbcbfa373d880928d0b0d8cb7bc136012
11 4100e890b7dee2ff5823663e37e45d1910f8d88c
12 405e
13 efb57270b215bcc0d6082d4bb711a27cdc3f9cc6
d 0x5dba6bc133e3cb2e86
p 0xffb4b12b9f8b57fc9c
q 0xf5486a5ae2e2e81454
? 0x2f42c1bc5b7338cdfc
>
```

As you can probably tell, the 5th element ([hah](https://en.wikipedia.org/wiki/The_Fifth_Element)) is `e`, followed by `d`, then `p`.  I don't know what #8 is, then #9 is `q`.

I am not sure about the others.  I tested a hypothesis, but it wasn't correct.