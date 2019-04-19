from web3 import (
    Web3,
    HTTPProvider,
)
from eth_wallet.exceptions import (
    InfuraErrorException
)


# TODO: for API KEY use dotenv or environment variables
# TODO: create new project with different API key this API KEY is already uploaded on Github
class Infura:
    """Abstraction over Infura node connection."""

    def __init__(self):
        self.w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/57caa86e6f454063b13d717be8cc3408"))
        # TODO: load environment variables as API key
        pass

    def get_web3(self):
        if not self.w3.isConnected():
            raise InfuraErrorException()

        return self.w3
