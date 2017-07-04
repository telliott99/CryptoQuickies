#### Getting the pycrypto module

From [here](https://pypi.python.org/pypi/pycrypto).

On macOS, I used [Homebrew](https://brew.sh) to install a an up-to-date Python 2.

```
> python
Python 2.7.13 (default, Jun 22 2017, 10:25:09) 
[GCC 4.2.1 Compatible Apple LLVM 8.1.0 (clang-802.0.42)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

My primary reason for that is that packages were failing to install for the system Python.  Now

```
> which pip
/usr/local/bin/pip
>
> pip install pycrypto
```

works fine.

#### Using the pycrypto module

The Python approach to ECB

```
>>> from Crypto.Cipher import AES
>>> k = "Thats my Kung Fu"
>>> cipher = AES.new(k, AES.MODE_ECB)
>>> 
>>> data = "Two One Nine Two"
>>> c = cipher.encrypt(data)
>>> 
>>> c
')\xc3P_W\x14 \xf6@"\x99\xb3\x1a\x02\xd7:'
>>> 
>>> import binascii as ba
>>> ba.hexlify(c)
'29c3505f571420f6402299b31a02d73a'
>>> 
>>> cipher.decrypt(c)
'Two One Nine Two'
>>>
```

That matches our AES implementation.

The Python approach to CBC

```
>>> iv = '\x00' * 16
>>> cipher = AES.new(k, mode=AES.MODE_CBC, IV=iv)
>>> data = "Two One Nine Two"
>>> c = cipher.encrypt(data)
>>> ba.hexlify(c)
'29c3505f571420f6402299b31a02d73a'
>>>
```

With a zeroed iv, the result is the same as ECB.  Change one bit:

```
>>> from Crypto.Cipher import AES
>>> import binascii as ba
>>>
>>> k = "Thats my Kung Fu"
>>> iv = '\x01' + '\x00' * 15
>>> cipher = AES.new(k, mode=AES.MODE_CBC, IV=iv)
>>>
>>> data = "Two One Nine Two"
>>> c = cipher.encrypt(data)
>>> ba.hexlify(c)
'b8c75fabde3d8c12ae992231fc004861'
>>> 
>>> cipher.decrypt(c)
'\xed\xb00\x8b\x91S\xe92\xe0\xf0LT\xdcT?\x0e'
>>> 
>>> cipher = AES.new(k, mode=AES.MODE_CBC, IV=iv)
>>> cipher.decrypt(c)
'Two One Nine Two'
>>> 
```

Note the second call to `AES.new`, required for decryption in ECB mode but not for CBC.

