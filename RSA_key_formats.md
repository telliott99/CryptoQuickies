#### RSA key formats

#### Overview

- Python's `rsa` module
    - Public:  PKCS #1 `BEGIN RSA PUBLIC KEY`
    - Private:  PKCS #1 `BEGIN RSA PRIVATE KEY`
- `openssl genrsa `
    - Public:  PKCS #8  `BEGIN PUBLIC KEY`
    - Private:  PKCS #1 `BEGIN PRIVATE KEY`
- `ssh-keygen`
    - Public:  `ssh-rsa`
    - Private:  PKCS #1 `BEGIN RSA PRIVATE KEY`

#### Details

Obtaining an RSA key pair from

* Python's `rsa` module

We used this module to construct key pairs with small values of *n* to make it easy to analyze them.  Here I'm using the values from this [writeup](RSA key intro.md).

```python
>>> import rsa
>>> n = 944871836856449473
>>> e = 65537
>>> pub_key = rsa.PublicKey(n=n,e=e)
>>> s = pub_key.save_pkcs1()
>>> print s
-----BEGIN RSA PUBLIC KEY-----
MA8CCA0c2+3yGXnBAgMBAAE=
-----END RSA PUBLIC KEY-----

>>>
>>> p = 961748941
>>> q = 982451653
>>> d = 8578341116816273
>>> priv_key = rsa.PrivateKey(n,e,d,p,q)
>>> s = priv_key.save_pkcs1()
>>> print s
-----BEGIN RSA PRIVATE KEY-----
MDkCAQACCA0c2+3yGXnBAgMBAAECBx559K8Hq5ECBDlTH80CBDqPBcUCBBEqrXkC
BCc4mh0CBACAc5Q=
-----END RSA PRIVATE KEY-----

>>>
```

We might also do

    >>> (pubkey, privkey) = rsa.newkeys(2048)

Note the headers

    `BEGIN RSA PUBLIC KEY`
    `BEGIN RSA PRIVATE KEY`
    
This format is `PKCS #1`, as the `rsa` method name `save_pkcs1` suggests.

(Also note that the `rsa` module *can* handle DER mode.  See below for an explanation of what this is).  

* openssl

The more usual way to generate keys is to use either `openssl` or `ssh-keygen`.

With `openssl`, it's a two-step process.   [Generate](https://www.madboa.com/geek/openssl/#how-do-i-generate-an-rsa-key) the private key first:

    > openssl genrsa -out kf.pem 1024
    Generating RSA private key, 1024 bit long modulus
    ..................++++++
    ....................++++++
    e is 65537 (0x10001)
    >
    
Take a look:  
    
    > cat kf.pem
    -----BEGIN RSA PRIVATE KEY-----
    MIICXAIBAAKBgQDfeogWvr5EsZeVjcd..

To encrypt with a passphrase, see [here](https://stackoverflow.com/questions/4294689/how-to-generate-an-openssl-key-using-a-passphrase-from-the-command-line).  Use `-passout pass:foobar` or `-passout file:passphrase.txt`.  

I used the `.pem` file type suffix at their suggestion (se below).

We then generate the public key from the private one:

    > openssl rsa -in kf.pem -pubout > kf.pub
    -----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4..

Note the header says `BEGIN PUBLIC KEY`.  No `RSA`.  This is PKCS #8.

The Python `rsa` module's `load_pkcs1` method will not load this key:

```python
>>> import rsa
>>> import utils as ut
>>> ut.load_data('kf.pub')
>>> pbk = rsa.PublicKey.load_pkcs1(data)
ValueError: No PEM start marker "-----BEGIN RSA PUBLIC KEY-----" found
```

instead, we need to use `load_pkcs1_openssl_pem`:

```python
>>> pbk = rsa.PublicKey.load_pkcs1_openssl_pem(data)
>>> pbk.e
65537
>>>
```

* ssh

The `ssh-keygen` utility gives both private and public keys at the same time.  We choose not to employ a passphrase.
    
    ssh-keygen -b 1024 -t rsa -f kf -N ''

* `-b` is the key size in bits (default __)
* `-t` type
* `-f` output filename
* `-N` specify (or change) passphrase


There is an SHA256 fingerprint:

    SHA256:eEcZzyiipEfna2bHaCBFnRL6abFPAUAM0VpBzZkjv0A

and ASCII art:

```
+---[RSA 1024]----+
|oB==+= .  .      |
|  EoB.o    *     |
| +.o=o+ . + o    |
|. .*.B + o       |
|  o.O.+ S .      |
|   +.+ = .       |
|      O o        |
|     = .         |
|                 |
+----[SHA256]-----+
>
```

The private key starts with:

    -----BEGIN RSA PRIVATE KEY-----
    MIICXAIBAAKBgQDdTybfVtOLDbU4pxk

The first 15 characters are the same as the `openssl` private key.

The public key looks different:

    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAA..
    
I analyzed the information in this format on the [blog](http://telliott99.blogspot.com/2011/08/dissecting-rsa-keys-in-python-2.html) and in a write-up in this repo ([RSA_key_ssh.md](RSA_key_ssh.md)).

Although the private keys generated by these three methods look similar, the public keys are all different.  See the Overview at the top.
    
Python's `rsa` module's `load_pkcs1` method will load the `ssh-keygen` **private** key:

```python
>>> data = ut.load_data('kf')
>>> privk = rsa.PrivateKey.load_pkcs1(data)
>>> privk.p
128938055904032426797534639781850323
```

but a similar approach for the **public** key fails.  That's because the public key is a special format.
    
#### Converting `ssh-rsa` to PKCS #1

Luckily, `ssh-keygen` will convert between different formats --- [docs](http://man.openbsd.org/OpenBSD-current/man1/ssh-keygen.1#NAME)

Example:

    ssh-keygen -e -m pem -f kf.pub

* `-e` export
* `-m` mode:  RFC4716 (default), PKCS8, or PEM

The output modes are

* PEM (PKCS #1)   `-----BEGIN RSA PUBLIC KEY-----`
* PKCS #8         `-----BEGIN PUBLIC KEY-----`
* RFC4716        `---- BEGIN SSH2 PUBLIC KEY ----`

So if I choose PEM mode and paste the resulting data into the interpreter (`s = '''data'''`)

```python
>>> s = '''-----BEGIN RSA PUBLIC KEY-----...
>>> pbk = rsa.PublicKey.load_pkcs1(s)
>>> pbk.e
65537
>>>
```

In summary, `ssh-keygen` has a special format for the public key, but we can easily convert to PEM (PKCS1) or PKCS8 if needed.

#### General discussion of formats

There are several different format specifications for RSA public/private key pairs.

Public key formats [include](https://www.cryptosys.net/pki/rsakeyformats.html)
:

- PKCS #1 RSAPublicKey
    - PEM header: `BEGIN RSA PUBLIC KEY`
- PKCS #8 SubjectPublicKeyInfo 
    - PEM header: `BEGIN PUBLIC KEY`
    - sometimes called X.509, because it is used for certificates
- OpenSSH

The actual data for public keys of these two types is exactly the same.  The difference is the extra metadata on the front end of the PKCS #8 base64 data.  If you remove 32 base64 characters (and switch `BEGIN PUBLIC RSA KEY`, they should be identical.

Private key formats:

- PKCS #1 RSAPrivateKey
    - PEM header: `BEGIN RSA PRIVATE KEY`
- PKCS #8 PrivateKeyInfo
    - PEM header: `BEGIN PRIVATE KEY`

Apparently, `openssl` gave us a *different* format for the private key.

In addition, a private key may be encrypted:

- PKCS #8 EncryptedPrivateKeyInfo
    - PEM header: `BEGIN ENCRYPTED PRIVATE KEY`

As a simplification, we can ignore XML format, and consider just two types:  PKCS #1 and PKCS #8 (though remembering X.509 refers to a public key of this type).

Key data may be encoded in three ways:

* PEM (base 64 format)
* DER (binary)
* XML

Again, we ignore DER and XML, and just consider base64 or PEM.

#### References

DER stands for Distinguished Encoding Rules.  People may talk about DER-encoded data.  In DER, the actual bytes of the key are present as is.

However, it is fair to call it an encoding because there are additional bytes of metadata to conform to [ASN.1 format](https://en.wikipedia.org/wiki/Abstract_Syntax_Notation_One).

[stackoverflow answer 2](https://stackoverflow.com/questions/18039401/how-can-i-transform-between-the-two-styles-of-public-key-format-one-begin-rsa).

PEM stands for Privacy Enhanced Mail  [here](https://en.wikipedia.org/wiki/Privacy-enhanced_Electronic_Mail).  A PEM-encoded key has the key bytes (and other data) encoded in base64.

Another great resource is [this](https://tls.mbed.org/kb/cryptography/asn1-key-structures-in-der-and-pem)


http://stuvel.eu/rsa 

http://stuvel.eu/files/python-rsa-doc/reference.html

