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

The private key is already in PEM format:

```
> openssl rsa -inform pem -in kf -text -noout
Private-Key: (1024 bit)
modulus:
    00:f5:00:42:9c:2d:77:bd:88:44:7a:1e:ab:3d:61:
    dc:f0:74:c5:89:98:40:e3:8b:5d:96:34:e1:c3:90:
    1b:ef:4c:af:44:e1:89:c0:31:c8:eb:8b:26:e2:1c:
    83:43:40:2f:e2:72:c0:a5:23:d1:7a:b7:a5:b4:ba:
    4f:93:07:a3:83:d5:b2:57:f9:2a:76:81:d0:0e:9a:
    a1:15:da:05:7e:15:af:4b:77:29:fa:b0:31:0f:10:
    fd:74:9c:ca:df:a6:14:99:af:a0:a6:0a:b4:cf:4c:
    09:b9:13:76:5b:89:a1:99:29:34:be:17:5d:c0:16:
    6a:e5:cb:4d:ad:d6:3e:38:ab
publicExponent: 65537 (0x10001)
privateExponent:
    5d:ba:6b:c1:33:e3:cb:2e:86:83:f1:97:b1:33:ef:
    42:4e:6a:03:e9:ab:69:61:b7:bb:ef:1f:2f:a1:c2:
    0e:1a:58:33:11:d5:91:21:7a:ac:21:e0:0e:40:ba:
    36:d0:27:81:8a:45:08:e8:5b:0b:87:96:6d:3d:99:
    93:b6:28:67:57:7f:fe:50:1e:d8:89:ce:83:a8:2f:
    af:e6:86:c4:54:f8:fd:e8:4d:5f:c7:bf:96:7c:34:
    27:a5:b5:2f:4e:6e:81:39:37:73:30:1d:85:d9:10:
    05:bd:7b:a3:f3:9e:2f:41:63:e1:5b:01:b1:8c:04:
    c9:4c:9c:51:69:0a:86:81
prime1:
    00:ff:b4:b1:2b:9f:8b:57:fc:9c:ab:61:94:c5:e6:
    cf:96:e9:cd:7a:4c:02:50:c1:61:b6:6d:ac:6f:8e:
    86:7c:9d:1b:16:70:b1:86:b1:ce:b2:1f:51:53:4a:
    d3:34:0e:74:28:7e:55:f0:a5:0d:8d:39:66:33:be:
    12:28:54:cc:1f
prime2:
    00:f5:48:6a:5a:e2:e2:e8:14:54:22:05:96:be:48:
    64:b2:18:c7:fb:1e:41:58:be:9a:48:51:a9:86:a1:
    96:0f:d7:11:b7:28:a3:e5:b3:0d:c4:54:ef:35:9e:
    5d:dd:a3:c7:65:7a:bf:ba:8a:2c:1b:2e:57:0f:e8:
    2c:b2:5d:41:f5
exponent1:
    64:1d:1f:bc:bf:a3:73:d8:80:92:8d:0b:0d:8c:b7:
    bc:13:60:12:c0:cd:ab:46:7b:76:4c:6c:55:e5:0c:
    7c:9f:9a:2a:68:06:e9:80:96:37:a1:11:5b:36:11:
    88:f1:1b:c3:7a:eb:34:e3:ba:71:8f:86:97:3d:94:
    a8:5b:c2:eb
exponent2:
    00:e8:90:b7:de:e2:ff:58:23:66:3e:37:e4:5d:19:
    10:f8:d8:8c:4c:ea:bb:f4:e4:0c:2f:03:d6:e4:43:
    33:a0:63:40:75:d4:bf:ca:1c:42:b2:64:01:c7:6a:
    17:ff:fd:b9:22:dc:07:0c:5c:d4:43:15:66:11:3c:
    07:9d:3a:d5:3d
coefficient:
    5e:02:ef:b5:72:70:b2:15:bc:c0:d6:08:2d:4b:b7:
    11:a2:7c:dc:3f:9c:c6:33:74:28:93:09:f0:cd:af:
    6f:b1:c2:7e:31:be:b5:c4:cd:98:71:4e:0c:76:0c:
    29:f2:3b:78:bc:b9:38:d8:ea:31:35:e3:76:af:a6:
    b4:5c:90:ec
>
```

Alternatively, we could use the `rsa` module:

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