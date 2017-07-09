### AES from the command line


Recall to encrypt  [msg.txt](msg.txt) from the commmand line we did:

```
> openssl aes-128-ecb -e -nopad -K "5468617473206d79204b756e67204675" -in msg.txt | xxd -p
29c3505f571420f6402299b31a02d73a
```

Save to a file:

```
> openssl aes-128-ecb -e -nopad -K "5468617473206d79204b756e67204675" -in msg.txt > cipher.bin
```

Decrypt:

```
> openssl aes-128-ecb -d -nopad -K "5468617473206d79204b756e67204675" -in cipher.bin
Two One Nine Two>
```

#### read key from a file


First write the key to `key.txt`:

```
> printf "Thats my Kung Fu" > key.txt
> hexdump -C key.txt
00000000  54 68 61 74 73 20 6d 79  20 4b 75 6e 67 20 46 75  |Thats my Kung Fu|
00000010
>
```

[key.txt](key.txt)

Now use it:

```
> openssl aes-128-ecb -e -nopad -kfile key.txt -in msg.txt | xxd -p
53616c7465645f5f0f523358c4af8b715d30492e363e825b10de0cf63386
e238
>
```

So here's a problem.  From the command line with `-K` and the password hex data we got

```
29c3505f571420f6402299b31a02d73a
```

I know this is the correct result (see above)

Furthermore, if I change the name of the file, the result changes:

```
> openssl aes-128-ecb -e -nopad -kfile key.orig.txt -in msg.txt | xxd -p
53616c7465645f5f4c6826bec38da95804079a9a8007639535c2f2578f50
772d
>
```

There is clearly some kind of issue with block size since the output is 32-bytes using the key file approach.

#### using `-pass`

According to [this](https://wiki.openssl.org/index.php/Enc) the `-kfile` option is deprecated.

```
> openssl aes-128-ecb -e -nopad -pass pass:key.txt -in msg.txt | xxd -p
53616c7465645f5f00d67281f5b5c995ab310a241ea9f8947ee8b8917f96
f466
>
```

Yet another incorrect result!