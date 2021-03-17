import json
import logging
import pathlib
from typing import NoReturn, Union, Type, Dict, Any

from web3 import Web3
from web3.contract import ContractConstructor, Contract, ContractFunction

__all__ = [
    'ContractException',
    'W3ProviderNotConnectedException',
    'FunctionNotFoundException',
    'ContractWrapper'
]


class ContractException(Exception):
    pass


class W3ProviderNotConnectedException(ContractException):
    pass


class FunctionNotFoundException(ContractException):
    pass


class ContractWrapper:
    PROJECT_ROOT = pathlib.Path(__file__).parent.parent

    def __init__(self, infura_key: str, metamask_private_key: str, timeout: int = 600) -> None:
        logging.info("Initialized Contract Wrapper")

        self._infura_key = infura_key
        self._metamask_private_key = metamask_private_key

        self._w3 = Web3(Web3.WebsocketProvider(f'wss://ropsten.infura.io/ws/v3/{self._infura_key}'))
        self._account = self._w3.eth.account.privateKeyToAccount(self._metamask_private_key)
        self._contract_data = None

        self._timeout = timeout

        self._prepare()

    def _prepare(self) -> NoReturn:
        self._read_contract_data()

        if not self.ready_check():
            raise W3ProviderNotConnectedException(
                f'w3.py is not connected to the websocket provider: {self._infura_key}'
            )

        logging.info("Contract Wrapper Initialized Successfully")

    def _read_contract_data(self) -> NoReturn:
        with open(self.PROJECT_ROOT / 'truffle' / 'Contract.json') as input_file:
            self._contract_data = json.load(input_file)

    def _build_contract(self, address: str = None) -> Union[Type[Contract], Contract]:
        return self._w3.eth.contract(
            abi=self._contract_data['abi'],
            bytecode=self._contract_data['bytecode'],
            address=address
        )

    def _build_transaction(self, contract: Union[ContractConstructor, ContractFunction]) -> Dict:
        construct_txn = contract.buildTransaction({
            'from': self._account.address,
            'nonce': self._w3.eth.getTransactionCount(self._account.address),
            'gas': 5500000,
            'gasPrice': self._w3.toWei('1', 'gwei')
        })

        signed = self._account.signTransaction(construct_txn)

        tx_hash = self._w3.eth.sendRawTransaction(signed.rawTransaction)

        logging.info(f"Transaction building started: {tx_hash.hex()}")

        receipt = self._w3.eth.waitForTransactionReceipt(tx_hash, timeout=self._timeout)

        logging.info(f"Transaction was built successfully: {tx_hash.hex()}")

        return {
            'tx_hash': tx_hash.hex(),
            'receipt': receipt
        }

    @staticmethod
    def _function_check(contract: Contract, function_name: str) -> bool:
        return function_name in list(map(lambda x: x.fn_name, contract.all_functions()))

    def ready_check(self) -> bool:
        return self._w3.isConnected()

    def create(self, buyer: str, seller: str, solver: str, value: int, item_id: str) -> Dict:
        logging.info(f"Building contract with arguments = [{buyer}, {seller}, {solver}, {value}, {item_id}]")

        contract = self._build_contract()
        result = self._build_transaction(
            contract.constructor(buyer, seller, solver, value, item_id)
        )

        logging.info(f"Contract was built successfully: {result['tx_hash']}")

        return result

    def call(self, address: str, function_name: str) -> Any:
        contract = self.get_contract(address)

        logging.info(f"Called contract function with args: address='{address}',fn='{function_name}'")

        if self._function_check(contract, function_name):
            return contract.get_function_by_name(function_name).__call__().call()
        else:
            raise FunctionNotFoundException

    def build(self, address: str, function_name: str) -> Dict:
        contract = self.get_contract(address)

        logging.info(f"Called building contract with args: address='{address}',fn='{function_name}'")

        if self._function_check(contract, function_name):
            return self._build_transaction(contract.get_function_by_name(function_name).__call__())
        else:
            raise FunctionNotFoundException

    def send(self, address: str) -> Dict:
        logging.info(f"Sending contract, address='{address}'")

        result = self.build(address, 'sent')

        logging.info(f"Contract was sent successfully: {result['tx_hash']}")

        return result

    def confirm(self, address: str) -> Dict:
        logging.info(f"Confirming receiving contract, address='{address}'")

        result = self.build(address, 'confirmReceived')

        logging.info(f"Contract receiving was confirmed successfully: {result['tx_hash']}")

        return result

    def get_contract(self, address: str) -> Union[Type[Contract], Contract]:
        return self._build_contract(address)

# if __name__ == '__main__':
# wrapper = ContractWrapper(infura, metamask, timeout=10000)

# print(wrapper.confirm('0xc56BF879976E26600C30186Fe3bB20bEfc58d4C7'))

# print(wrapper.call('0xAC4Ec8a1d878923388395381BDA9FC2E7760b6c0', 'buyer'))

# print(
#     wrapper.create(
#         "0xD36549D00D81F35f7e44d48A46A966616fB2f945",
#         "0xD36549D00D81F35f7e44d48A46A966616fB2f945",
#         "0xD36549D00D81F35f7e44d48A46A966616fB2f945",
#         100,
#         "1"
#     )
# )
