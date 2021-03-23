# Smart Contract API

### Contract Wrapper object

New contract wrapper object can be created with:

```python
from contracts_api import ContractWrapper

wrapper = ContractWrapper('<INFURA_KEYY>', '<METAMASK_PRIVATE_KEY>', timeout=600)  # default timeout value is 600 
```

#### Contract creation

Then you can submit a new smart contract with command:

```python
from contracts_api import ContractWrapper

wrapper = ContractWrapper('<INFURA_KEYY>', '<METAMASK_PRIVATE_KEY>', timeout=600)  # default timeout value is 600

seller_address = '0xC819A40FD16b77608289dcB23AdD77Ca2D81F66D'
solver_address = '0x1241fd2a59AB1168B803C32318B7855726b70356'

wrapper.create(
    seller_address,  # str
    solver_address,  # str
    100,  # price of the product: should be int
    '1'  # product id: should be int casted to string
)
```

This function returns dict like object which contains:

```python
from web3.types import TxReceipt

{
    'tx_hash': '<hash of the transaction that was submitted>',
    'receipt': TxReceipt
}
# then contract address can be reached with: result["receipt"]["contractAddress"]  
```

_Note_: smart contract creation should be asynchronously called

#### Contract sending functionality (after the seller sent his product)

```python
from contracts_api import ContractWrapper

wrapper = ContractWrapper('<INFURA_KEYY>', '<METAMASK_PRIVATE_KEY>', timeout=600)  # default timeout value is 600

wrapper.send(
    '0xAC4Ec8a1d878923388395381BDA9FC2E7760b6c0',  # smart contract address: str
)
```

This function returns dict like object which contains:

```python
from web3.types import TxReceipt

{
    'tx_hash': '<hash of the transaction that was submitted>',
    'receipt': TxReceipt
}
```

_Note_: smart contract sending should be asynchronously called

#### Contract receiving confirmation functionality (after the buyer received his product)

```python
from contracts_api import ContractWrapper

wrapper = ContractWrapper('<INFURA_KEYY>', '<METAMASK_PRIVATE_KEY>', timeout=600)  # default timeout value is 600

wrapper.confirm(
    '0xAC4Ec8a1d878923388395381BDA9FC2E7760b6c0',  # smart contract address: str
)
```

This function returns dict like object which contains:

```python
from web3.types import TxReceipt

{
    'tx_hash': '<hash of the transaction that was submitted>',
    'receipt': TxReceipt
}
```

_Note_: smart contract receiving confirmation should be asynchronously called

#### Wrapper additional functions

##### call()

Call the smart contract function by name and returns its result

```python
from contracts_api import ContractWrapper

wrapper = ContractWrapper('<INFURA_KEYY>', '<METAMASK_PRIVATE_KEY>', timeout=600)  # default timeout value is 600

wrapper.call(
    '0xAC4Ec8a1d878923388395381BDA9FC2E7760b6c0',  # smart contract address: str
    'function_name'  # smart contract function, should be in .sol file: str
)
```

##### build()

Call the smart contract function by name, build the transaction and send it to the blockchain

```python
from contracts_api import ContractWrapper

wrapper = ContractWrapper('<INFURA_KEYY>', '<METAMASK_PRIVATE_KEY>', timeout=600)  # default timeout value is 600

wrapper.build(
    '0xAC4Ec8a1d878923388395381BDA9FC2E7760b6c0',  # smart contract address: str
    'function_name'  # smart contract function, should be in .sol file: str
)
```

This function returns dict like object which contains:

```python
from web3.types import TxReceipt

{
    'tx_hash': '<hash of the transaction that was submitted>',
    'receipt': TxReceipt
}
```

_Note_: smart contract build function should be asynchronously called

##### get_contract

Get smart contract object by smart contract address

```python
from contracts_api import ContractWrapper

wrapper = ContractWrapper('<INFURA_KEYY>', '<METAMASK_PRIVATE_KEY>', timeout=600)  # default timeout value is 600

wrapper.get_contract(
    '0xAC4Ec8a1d878923388395381BDA9FC2E7760b6c0',  # smart contract address: str
)
# returns 
from web3.contract import Contract
Contract() # object 
```

##### ready_check()

Check if wrapper ready for working

```python
from contracts_api import ContractWrapper

wrapper = ContractWrapper('<INFURA_KEYY>', '<METAMASK_PRIVATE_KEY>', timeout=600)  # default timeout value is 600

wrapper.ready_check()  # returns True if w3.py successfully connected to the infura node, False otherwise
```
