#### Using the pycrypto module

Python approach to ECB

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

Python approach to CBC

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
>>> cipher = AES.new(k, mode=AES.MODE_CBC, IV=iv)
>>> c = cipher.encrypt(data)
>>> cipher = AES.new(k, mode=AES.MODE_CBC, IV=iv)
>>> cipher.decrypt(c)
'Two One Nine Two'
>>> 
```

Note the second call to `AES.new`, required for ECB mode but not for CBC.

