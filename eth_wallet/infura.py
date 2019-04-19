from web3 import Web3, HTTPProvider
# from eth_wallet.api import WalletAPI

# TODO: for API KEY use dotenv or environment variables
# TODO: create new project with different API key this API KEY is already uploaded on Github
# w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/57caa86e6f454063b13d717be8cc3408"))
# print(w3.isConnected())
# # print(w3.eth.blockNumber)
# # print(w3.eth.getBlock('latest'))
#
# wallet = WalletAPI().get_account('ahoj')
# balance = w3.fromWei(w3.eth.getBalance(wallet.get_account_address()), 'ether')
# print(balance)


class InfuraErrorException(RuntimeError):
    """Exception if problem with Infura node occur."""
    def __init__(self, arg):
        self.args = arg


class Infura:
    """Abstraction over Infura node connection."""

    def __init__(self):
        self.w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/57caa86e6f454063b13d717be8cc3408"))
        # TODO: load environment variables as API key
        pass

    def get_web3(self):
        if not self.w3.isConnected():
            raise InfuraErrorException(RuntimeError)

        return self.w3
