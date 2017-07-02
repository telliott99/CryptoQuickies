### AES from the command line

Recall that ECB (electronic code book) modes encrypts each block of plaintext with the same key.

[wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_Codebook_.28ECB.29)

CBC (cipher block chaining) `XOR`s each block of plaintext with the previous ciphertext before encrypting, also re-using the same key for each block.

CBC mode requires an initialization vector or IV which is used for the XOR of the first block of plaintext.

Both of these modes are implemented as part of DES or AES.  AES, the advanced encryption standard, is the newer protocol.

### ECB

Let's use AES on the command line with `openssl`, starting with ECB mode.  The first part of the command is

```
openssl aes-128-ecb -e -nopad
```

The flag `-e` is for encrypt, it's the default mode but I am self-documenting.

The `-nopad` is optional.  The default is to pad everything, even if the input is an exact multiple of the block size, 16 bytes.  

I suppress this but then it is required to provide a message that is an exact multiple of the block size.

#### key

The second part is

```
-K "5468617473206d79204b756e67204675" -in msg.txt
```

The plaintext message is read from a textfile.

```
> echo -n "Two One Nine Two" > msg.txt
> hexdump -C msg.txt
00000000  54 77 6f 20 4f 6e 65 20  4e 69 6e 65 20 54 77 6f  |Two One Nine Two|
00000010
>
```

[msg.txt](msg.txt)

The key is `'Thats my Kung Fu'`.  We can get it as hex using `xxd`:

```
> key="Thats my Kung Fu"
> xxd -p  <<< "$key"
5468617473206d79204b756e672046750a
>
```

or just

```
> xxd -p <<< "Thats my Kung Fu"
5468617473206d79204b756e672046750a
>
```

`xxd` has put a newline `0a` at the end of the hex output.  There are fancy options to remove it (like `tr -d "\n"`), but I just cut-and-paste.

#### Time to encrypt

```
> openssl aes-128-ecb -e -nopad -K "5468617473206d79204b756e67204675" -in msg.txt | xxd -p
29c3505f571420f6402299b31a02d73a
```

We examine the output.  Note the use of `xxd` to convert the raw bytes to hex.

```
29c3505f571420f6402299b31a02d73a
```

Or we could write them to a file.

```
> openssl aes-128-ecb -e -nopad -K "5468617473206d79204b756e67204675" -in msg.txt -out cipher.bin
> hexdump -C cipher.bin
00000000  29 c3 50 5f 57 14 20 f6  40 22 99 b3 1a 02 d7 3a  |).P_W. .@".....:|
00000010
>
```


#### decrypt

```
> openssl aes-128-ecb -d -nopad -K "5468617473206d79204b756e67204675" -in cipher.bin | xxd -p
54776f204f6e65204e696e652054776f
>
>
> openssl aes-128-ecb -d -nopad -K "5468617473206d79204b756e67204675" -in cipher.bin -out out.txt
> cat out.txt
Two One Nine Two>
>
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
53616c7465645f5f3032a065cf41c9ca4264a0a0e5325a31e29743292252
4e06
>
```

So here's a problem.  From the command line with `-K` and the password hex data we got

```
29c3505f571420f6402299b31a02d73a
```

Here we got

```
53616c7465645f5f3032a065cf41c9ca4264a0a0e5325a31e29743292252
4e06
```

And I got something a bit different with

```
> openssl aes-128-ecb -e -nopad -pass file:key.txt -in msg.txt | xxd -p
53616c7465645f5f6915b2a521f0ce9076e8b1ff8f5cb48f26577dfe57a7
33e4
>
```

I haven't figured this out!  There is clearly some kind of issue with block size since the output is 32-bytes using the key file approach.

### CBC

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

Since we chose an iv with null bytes, the result is exactly the same as ECB mode.

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

I only wrote 8 bytes so we get two copies:

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

