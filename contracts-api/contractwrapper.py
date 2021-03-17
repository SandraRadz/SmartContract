import json
import logging
import pathlib

from web3 import Web3


class ContractException(Exception):
    pass


class W3ProviderNotConnectedException(ContractException):
    pass


class FunctionNotFoundException(ContractException):
    pass


class ContractWrapper:
    PROJECT_ROOT = pathlib.Path(__file__).parent.parent

    def __init__(self, infura_key, metamask_private_key, timeout=600):
        logging.info("Initialized Contract Wrapper")

        self._infura_key = infura_key
        self._metamask_private_key = metamask_private_key

        self._w3 = Web3(Web3.WebsocketProvider(f'wss://ropsten.infura.io/ws/v3/{self._infura_key}'))
        self._account = self._w3.eth.account.privateKeyToAccount(self._metamask_private_key)
        self._contract_data = None

        self._timeout = timeout

        self._prepare()

    def _prepare(self):
        self._read_contract_data()

        if not self.ready_check():
            raise W3ProviderNotConnectedException(
                f'w3.py is not connected to the websocket provider: {self._infura_key}'
            )

        logging.info("Contract Wrapper Initialized Successfully")

    def _read_contract_data(self):
        with open(self.PROJECT_ROOT / 'truffle' / 'Contract.json') as input_file:
            self._contract_data = json.load(input_file)

    def _build_contract(self, address=None):
        return self._w3.eth.contract(
            abi=self._contract_data['abi'],
            bytecode=self._contract_data['bytecode'],
            address=address
        )

    def _call(self, function_name):
        pass

    def _build_transaction(self, contract):
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
    def _function_check(contract, function_name):
        return function_name in list(map(lambda x: x.fn_name, contract.all_functions()))

    def ready_check(self):
        return self._w3.isConnected()

    def create(self, buyer, seller, solver, value, item_id):
        logging.info(f"Building contract with arguments = [{buyer}, {seller}, {solver}, {value}, {item_id}]")

        contract = self._build_contract()
        result = self._build_transaction(
            contract.constructor(buyer, seller, solver, value, item_id)
        )

        logging.info(f"Contract was built successfully: {result['tx_hash']}")

        return result

    def call(self, address, function_name):
        contract = self.get_contract(address)

        logging.info(f"Called contract function with args: address='{address}',fn='{function_name}'")

        if self._function_check(contract, function_name):
            return contract.get_function_by_name(function_name).__call__().call()
        else:
            raise FunctionNotFoundException

    def build(self, address, function_name):
        contract = self.get_contract(address)

        logging.info(f"Called building contract with args: address='{address}',fn='{function_name}'")

        if self._function_check(contract, function_name):
            return self._build_transaction(contract.get_function_by_name(function_name).__call__())
        else:
            raise FunctionNotFoundException

    def send(self, address):
        logging.info(f"Sending contract, address='{address}'")

        result = self.build(address, 'sent')

        logging.info(f"Contract was sent successfully: {result['tx_hash']}")

        return result

    def confirm(self, address):
        logging.info(f"Confirming receiving contract, address='{address}'")

        result = self.build(address, 'confirmReceived')

        logging.info(f"Contract receiving was confirmed successfully: {result['tx_hash']}")

        return result

    def get_contract(self, address):
        return self._build_contract(address)


if __name__ == '__main__':
    metamask = 'a3d3eb24d66c13a91f085e8431526540c243f88d147613a24edb05110d732a6a'
    infura = 'bc71a2e7b3884039b7903a2870ca56b3'

    wrapper = ContractWrapper(infura, metamask, timeout=10000)

    # print(wrapper.call('0xAC4Ec8a1d878923388395381BDA9FC2E7760b6c0', 'state'))

    # contract = wrapper.get_contract('0xAC4Ec8a1d878923388395381BDA9FC2E7760b6c0')

    # print(contract.get_function_by_name('state').__call__().call())

    # print(wrapper.confirm("0xAC4Ec8a1d878923388395381BDA9FC2E7760b6c0"))

    print(
        wrapper.create(
            "0xD36549D00D81F35f7e44d48A46A966616fB2f945",
            "0xD36549D00D81F35f7e44d48A46A966616fB2f945",
            "0xD36549D00D81F35f7e44d48A46A966616fB2f945",
            100,
            "1"
        )
    )
