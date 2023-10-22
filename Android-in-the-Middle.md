# Android-in-the-Middle

The shared memory is always one if M is one:

> shared_secret = pow(M, c, p)

From there,
>key = hashlib.md5(long_to_bytes(shared_secret)).digest()

can be calculated as
>key = hashlib.md5(long_to_bytes(1)).digest()

And the message we need to send the server to get the flag is "message" in:
>   cipher = AES.new(key, AES.MODE_ECB)
>
> message = cipher.encrypt(b"Initialization Sequence - Code 0")
    
    DEBUG MSG - Generating The Global DH Parameters
    DEBUG MSG - g = 2, p = 10177459997049772558637057109490700048394574760284564283959324525695097805837401714582821820424475480057537817583807249627119267268524840254542683041588432363128111683358536204391767254517057859973149680238170237977230020947732558089671785239121778309357814575486749623687357688511361367822815452806637006568922401890961240475060822815400430220536180181951862931844638638933951683988349468373510128406899660648258602475728913837826845743111489145006566908004165703542907243208106044538037004824530893555918497937074663828069774495573109072469750423175863678445547058247156187317168731446722852098571735569138516533993
    DEBUG MSG - Calculation Complete
    DEBUG MSG - Generating The Public Key of CPU...
    DEBUG MSG - Calculation Complete
    DEBUG MSG - Public Key is: ???
    
    Enter The Public Key of The Memory: 1
    
    DEBUG MSG - The CPU Calculates The Shared Secret
    DEBUG MSG - Calculation Complete
    
    Enter The Encrypted Initialization Sequence: 7fd4794e77290bf65808e95467f284966d71995c16e83da2192aecfd2d0df7a4
    
    DEBUG MSG - Reseting The Protocol With The New Shared Key
    DEBUG MSG - HTB{7h15_p2070c0l_15_pr0tec73d_8y_D@nb3er_c0pyr1gh7_1aws}
