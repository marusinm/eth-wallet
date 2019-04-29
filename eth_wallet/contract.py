import time
from eth_wallet.infura import (
    Infura,
)
from eth_wallet.utils import (
    get_abi_json,
)


class Contract:
    """Abstraction over ERC20 tokens"""

    # fitcoin_address = '0x19896cB57Bc5B4cb92dbC7D389DBa6290AF505Ce'
    # binancecoin_address = '0x64BBF67A8251F7482330C33E65b08B835125e018'
    # my_address = '0xc3519C4560BcfE3Ac0b137f1067d1655ed65FEa4'
    # metamask_address = '0xAAD533eb7Fe7F2657960AC7703F87E10c73ae73b'

    def __init__(self, configuration, address):
        """
        Constructor
        :param address: contract address or ESN name
        :type address: string
        """
        self.conf = configuration
        self.address = address

        self.w3 = Infura().get_web3()
        self.contract = self.w3.eth.contract(address=address, abi=get_abi_json())
        self.contract_decimals = self.contract.functions.decimals().call()

    def add_new_contract(self, contract_symbol, contract_address):
        """
        Add ERC20 token to the wallet
        :param contract_symbol: token symbol
        :param contract_address: contract address
        :return:
        """
        self.conf.add_contract_token(contract_symbol, contract_address)

    def get_balance(self, wallet_address):
        """
        Get wallet's ballance of self.contract
        :param wallet_address: this wallet address
        :type wallet_address: string
        :return: balance as decimal number
        """
        return self.contract.functions.balanceOf(wallet_address).call() / (10 ** self.contract_decimals)

    def get_decimals(self):
        """
        Returns the number of decimals
        :return: integer
        """
        return self.contract_decimals

    def get_erc20_contract(self):
        """
        Returns w3.eth.contract instance
        :return:
        """
        return self.contract


# w3 = Infura().get_web3()
#
# contract = w3.eth.contract(address=fitcoin_address, abi=get_abi_json())
# # contract = w3.eth.contract(address=binancecoin_address, abi=get_abi_json())
# print(contract.functions.balanceOf(my_address).call() / 10**18)
# print(contract.functions.decimals().call())

#
# nonce = w3.eth.getTransactionCount(my_address)
# txn_dict = contract.functions.transfer(metamask_address, 2 * (10**18)).buildTransaction({
#     'chainId': 3,  # Ropsten
#     'gas': 140000,
#     'gasPrice': w3.toWei('40', 'gwei'),
#     # 'gasPrice': w3.eth.gasPrice * 10 * 2,
#     'nonce': nonce,
# })
#
# signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=priv_key)
# tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
#
# print('Pending', end='', flush=True)
# while True:
#     tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
#     if tx_receipt is None:
#         print('.', end='', flush=True)
#         time.sleep(1)
#     else:
#         print('\nTransaction mined!')
#         break
# print(tx_hash.hex())

