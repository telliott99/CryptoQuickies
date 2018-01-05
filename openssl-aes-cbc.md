### AES from the command line

CBC (cipher block chaining) `XOR`s each block of plaintext with the previous ciphertext before encrypting, also re-using the same key for each block.

CBC mode requires an initialization vector or IV which is used for the XOR of the first block of plaintext.

Both of these modes are implemented as part of DES or AES.  AES, the advanced encryption standard, is the newer protocol.

### CBC mode

#### the iv

CBC requires an initialization vector, abbreviated iv.

```
> openssl aes-128-cbc -e -nopad -K "5468617473206d79204b756e67204675" -in msg.txt -iv "0000000000000000"| xxd -p
29c3505f571420f6402299b31a02d73a
>
```

One would have expected to need 16 bytes!  Check this out, `iv = ""` works:

```
> openssl aes-128-cbc -e -nopad -K "5468617473206d79204b756e67204675" -in msg.txt -iv ""| xxd -p
29c3505f571420f6402299b31a02d73a
>
> openssl aes-128-cbc -e -nopad -K "5468617473206d79204b756e67204675" -in msg.txt -iv "00000000000000000000000000000000"| xxd -p
29c3505f571420f6402299b31a02d73a
>
```

Apparently, the iv gets padded out to 16 with null bytes.

Since we chose an iv with null bytes, the result for this single block is exactly the same as ECB mode.

Making a change to the first byte gives a completely different result as we would expect.

```
> openssl aes-128-cbc -e -nopad -K "5468617473206d79204b756e67204675" -in msg.txt -iv "01"| xxd -p
b8c75fabde3d8c12ae992231fc004861
>
```

#### PKCS#7 padding

If we drop the `-nopad`

```
> openssl aes-128-cbc -e -K "5468617473206d79204b756e67204675" -in msg.txt -iv "0000000000000000"| xxd -p
29c3505f571420f6402299b31a02d73a5f5917ec376a3a269efadb6b2d61
e4e3
>
```
We get a second block from the padding.  The padding should be 16-bytes (this is 128-bit 16-byte AES), so two copies of

```
"\x10\x10\x10\x10\x10\x10\x10\x10"
```

We test this by putting back the `-nopad` and adding the pad to `msg.txt` in `msg2.txt`.

```
> printf "\x10\x10\x10\x10\x10\x10\x10\x10" > pad.txt
> 
```

I only wrote 8 bytes so we grab two copies:

```
> cat msg.txt pad.txt pad.txt > msg2.txt
> hexdump -C msg2.txt
00000000  54 77 6f 20 4f 6e 65 20  4e 69 6e 65 20 54 77 6f  |Two One Nine Two|
00000010  10 10 10 10 10 10 10 10  10 10 10 10 10 10 10 10  |................|
00000020
> openssl aes-128-cbc -e -nopad -K "5468617473206d79204b756e67204675" -in msg2.txt -iv "0000000000000000"| xxd -p
29c3505f571420f6402299b31a02d73a5f5917ec376a3a269efadb6b2d61
e4e3
>
```

That's a match.

#### base 64

One more useful option is to output in base64 mode:

```
> openssl aes-128-ecb -a -e -nopad -K "5468617473206d79204b756e67204675" -in msg.txt
KcNQX1cUIPZAIpmzGgLXOg==
>
```

```
> openssl aes-128-ecb -a -e -nopad -K "5468617473206d79204b756e67204675" -in msg.txt -out c.txt
> cat c.txt
KcNQX1cUIPZAIpmzGgLXOg==
> openssl aes-128-ecb -a -d -nopad -K "5468617473206d79204b756e67204675" -in c.txt 
Two One Nine Two>
> 
```
