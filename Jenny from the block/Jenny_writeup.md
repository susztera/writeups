# Jenny From The Block
  H T B { b 4 5 1 c _ b 1 0 c k _ c 1 p h 3 r _ 1 5 _ w 3 4 k ! ! ! }
  
  ...Yep. That's it. That's all I wrote for a write-up back then. The flag characters, divided by some whitespace - I believe I worked out each character separately for this challenge.
  
  But, I can see why, as the challenge was a block cipher with known plaintext of the same size as the encryption block. 
  This means I did a lot of brute forcing trying to see which bytes used as a key would result in the correct encrypted text. Was that the smart way to do it? Probably not.
  Was it time efficient in terms of the overall CTF to make a short script very quickly and leave it running in the background while I solved other challenges? Questionably, but I gambled on it.

  Observe the following code block from the challenge.

  ```python
response = b'Command executed: ' + command + b'\n' + output
password = os.urandom(32)
ct = encrypt(response, password)
```

```python
allowed_commands = [b'whoami', b'ls', b'cat secret.txt', b'pwd']
BLOCK_SIZE = 32


def encrypt_block(block, secret):
    enc_block = b''
    for i in range(BLOCK_SIZE):
        val = (block[i]+secret[i]) % 256
        enc_block += bytes([val])
    return enc_block


def encrypt(msg, password):
    h = sha256(password).digest()
    if len(msg) % BLOCK_SIZE != 0:
        msg = pad(msg, BLOCK_SIZE)
    blocks = [msg[i:i+BLOCK_SIZE] for i in range(0, len(msg), BLOCK_SIZE)]
    ct = b''
    for block in blocks:
        enc_block = encrypt_block(block, h)
        h = sha256(enc_block + block).digest()
        ct += enc_block

    return ct.hex()
```

Is that `Command executed: cat secret.txt` being the same length as our block size (32) I just spotted? 

> I looked into it for you, just for fun: the padding algorithm used here is from pycryptodome's `Crypto.Util.Padding` which uses the `pkcs7` padding algorithm. 
This means if the "+ output" part came after the padding in the program you technically still get 32 bytes of known plaintext because
> you calculate what the padding values are based on [this](https://www.ibm.com/docs/en/zos/3.1.0?topic=rules-pkcs-padding-method) chart.
Because of `Command executed: ` you will always only have 14 bytes to work with out of the 32-byte block length, so don't worry about the chart only speaking about up to 16 bytes.

And from then on - if memory serves me correctly - I tried all possible bytes against the known plaintext and ciphertext, and got the encryption key, `h`.
The variable `h` can then be calculated for each proceeding block because we will be in possession of the encrypted text and can calculate the decrypted text. 
Again, I think I went brute-force throughout but did some re-solving to be able to provide a complete write-up, and I believe [this](https://stackoverflow.com/questions/49226755/modulo-operator-in-decryption) was the
correct maths to decrypt that block cipher. 
