#### Hash algorithms

`md5`

```
> touch x.txt
> md5 x.txt
MD5 (x.txt) = d41d8cd98f00b204e9800998ecf8427e
> touch y.txt
> md5 y.txt
MD5 (y.txt) = d41d8cd98f00b204e9800998ecf8427e
>
```

```
> printf "abc" > x.txt
> md5 x.txt
MD5 (x.txt) = 900150983cd24fb0d6963f7d28e17f72
> printf "abcd" > y.txt
> md5 y.txt
MD5 (y.txt) = e2fc714c4727ee9395f324cd2e7f331f
>
```
`sha`

```
> openssl sha1 x.txt
SHA1(x.txt)= a9993e364706816aba3e25717850c26c9cd0d89d
> openssl sha x.txt
SHA(x.txt)= 0164b8a914cd2a5e74c4f7ff082c4d97f1edf880
>

```

For SHA256:

```
> openssl dgst -sha1 x.txt
SHA1(x.txt)= a9993e364706816aba3e25717850c26c9cd0d89d
> openssl dgst -sha256 x.txt
SHA256(x.txt)= ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
>
```

So which is the default?  It is just `SHA`!  Not 1 or 256 or whatever.