import json
import pathlib

from web3 import Web3


class ContractException(Exception):
    pass


class W3ProviderNotConnectedException(ContractException):
    pass


class ContractWrapper:
    PROJECT_ROOT = pathlib.Path(__file__).parent.parent

    def __init__(self, infura_key, metamask_private_key):
        self._infura_key = infura_key
        self._metamask_private_key = metamask_private_key

        self._w3 = Web3(Web3.WebsocketProvider(f'wss://ropsten.infura.io/ws/v3/{self._infura_key}'))
        self._account = self._w3.eth.account.privateKeyToAccount(self._metamask_private_key)
        self._contract_data = None

        self._prepare()

    def _prepare(self):
        self._read_contract_data()

        if not self.ready_check():
            raise W3ProviderNotConnectedException(
                f'w3.py is not connected to the websocket provider: {self._infura_key}'
            )

    def _read_contract_data(self):
        with open(self.PROJECT_ROOT / 'truffle' / 'Contract.json') as input_file:
            self._contract_data = json.load(input_file)

    def _build_contract(self, address=None):
        return self._w3.eth.contract(
            abi=self._contract_data['abi'],
            bytecode=self._contract_data['bytecode'],
            address=address
        )

    def ready_check(self):
        return self._w3.isConnected()

    def create(self, buyer, seller, solver, value, item_id):
        contract = self._build_contract()
        construct_txn = contract.constructor(
            buyer, seller, solver, value, item_id
        ).buildTransaction({
            'from': self._account.address,
            'nonce': self._w3.eth.getTransactionCount(self._account.address),
            'gas': 5500000,
            'gasPrice': self._w3.toWei('21', 'gwei')
        })

        signed = self._account.signTransaction(construct_txn)

        tx_hash = self._w3.eth.sendRawTransaction(signed.rawTransaction)

        receipt = self._w3.eth.waitForTransactionReceipt(tx_hash, timeout=600)

        return {
            'tx_hash': tx_hash.hex(),
            'receipt': receipt
        }


if __name__ == '__main__':
    metamask = 'a3d3eb24d66c13a91f085e8431526540c243f88d147613a24edb05110d732a6a'
    infura = 'bc71a2e7b3884039b7903a2870ca56b3'

    wrapper = ContractWrapper(infura, metamask)
    print(
        wrapper.create(
            "0xD36549D00D81F35f7e44d48A46A966616fB2f945",
            "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4",
            "0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2",
            100,
            "1"
        )
    )

    # print(w3.isConnected())

    # with open(PROJECT_ROOT / 'truffle' / 'Contract.json') as input_file:
    #     data = json.load(input_file)
    #
    # contract = w3.eth.contract(abi=data['abi'], bytecode=data['bytecode'])
    #
    # acct = w3.eth.account.privateKeyToAccount(METAMASK_PRIVATE_KEY)
    #
    # construct_txn = contract.constructor(
    #     "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4",
    #     "0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2",
    #     "1"
    # ).buildTransaction({
    #     'from': acct.address,
    #     'nonce': w3.eth.getTransactionCount(acct.address),
    #     'gas': 5500000,
    #     'gasPrice': w3.toWei('21', 'gwei')
    # })
    #
    # contract.functions.send().buildTransaction({
    #     'from': '0x5B38Da6a701c568545dCfcB03FcB875f56beddC4',
    #     'nonce': w3.eth.getTransactionCount(acct.address),
    #     'gas': 5500000,
    #     'gasPrice': w3.toWei('21', 'gwei')
    # })
    #
    # signed = acct.signTransaction(construct_txn)
    #
    # tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    #
    # # tx_hash = contract.constructor(
    # #     "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4",
    # #     "0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2",
    # #     "1"
    # # ).transact()
    #
    # # print(tx_hash)
    # try:
    #     print(tx_hash.hex())
    # except Exception:
    #     print('cant be decoded')
    #
    # print(w3.eth.waitForTransactionReceipt(tx_hash, timeout=600))
