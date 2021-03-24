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


class InvalidContractFunctionCall(ContractException):
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

    def _build_transaction(
            self,
            contract: Union[ContractConstructor, ContractFunction],
            opts: Union[None, dict] = None
    ) -> Dict:
        if opts is None:
            opts = {}

        construct_txn = contract.buildTransaction({
            'from': self._account.address,
            'nonce': self._w3.eth.getTransactionCount(self._account.address),
            'gas': 5500000,
            'gasPrice': self._w3.toWei('1', 'gwei'),
            **opts
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

    def create(self, seller: str, solver: str, value: int, item_id: str) -> Dict:
        logging.info(f"Building contract with arguments = [{seller}, {solver}, {value}, {item_id}]")

        contract = self._build_contract()
        result = self._build_transaction(
            contract.constructor(seller, solver, item_id),
            {'value': value}
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

        contract = self.get_contract(address)
        if contract.functions.state().call() != 0:
            raise InvalidContractFunctionCall("Contract state is not Created. Cannot call 'sent()' function on it.")

        result = self._build_transaction(contract.functions.sent())

        logging.info(f"Contract was sent successfully: {result['tx_hash']}")

        return result

    def confirm(self, address: str) -> Dict:
        logging.info(f"Confirming receiving contract, address='{address}'")

        contract = self.get_contract(address)

        if contract.functions.state().call() != 1:
            raise InvalidContractFunctionCall(
                "Contract state is not Locked. Cannot call 'confirmReceived()' function on it."
            )

        result = self._build_transaction(contract.functions.confirmReceived())

        logging.info(f"Contract receiving was confirmed successfully: {result['tx_hash']}")

        return result

    def get_contract(self, address: str) -> Union[Type[Contract], Contract]:
        return self._build_contract(address)


if __name__ == '__main__':
    infura = 'bc71a2e7b3884039b7903a2870ca56b3'
    metamask = 'a3d3eb24d66c13a91f085e8431526540c243f88d147613a24edb05110d732a6a'

    wrapper = ContractWrapper(infura, metamask, timeout=10000)

    # print(wrapper.send('0xE4EAB7DAa6582307118DD8b415a385A763A45eFA'))

    # print(wrapper.confirm('0xE4EAB7DAa6582307118DD8b415a385A763A45eFA'))

    # print(type(wrapper.get_contract('0xE4EAB7DAa6582307118DD8b415a385A763A45eFA').functions.state().call()))
    # print(wrapper.call('0xE4EAB7DAa6582307118DD8b415a385A763A45eFA', 'state'))

    # print(
    #     wrapper.create(
    #         "0x046db58752d0076CFE0B38ca0eBa1fb9Df53a0f7",
    #         "0x4DAAFf96dec0f269B4c2a8F870380e5d87735baf",
    #         1000,
    #         "1"
    #     )
    # )
