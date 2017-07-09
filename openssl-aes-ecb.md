### AES from the command line

Recall that ECB (electronic code book) modes encrypts each block of plaintext with the same key.

[wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_Codebook_.28ECB.29)

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

Note that the result matches what we got when implementing AES from scratch [here](../Crypto/AES4-encrypt.md), and we get the same result using the Python `pycrypto` module. [here](python-aes.md).


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
