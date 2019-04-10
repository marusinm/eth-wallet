from eth_account import (
    Account,
)
from eth_keys import (
    keys,
)


class WalletAccount:
    """
    Class defining the main wallet account
    """
    def __init__(self):
        self.account = None

    def create(self, extra_entropy=''):
        """
        Creates new account that means private key with an attached address using os.urandom CSPRNG
        :param extra_entropy: Add extra randomness to whatever randomness your OS can provide
        :return: object with private key
        """
        self.account = Account.create(extra_entropy)
        return self.account

    def get_account_private_key(self):
        """
        Returns account private key
        :return: private key
        """
        return self.account.privateKey  # to print private key in hex use account.privateKey.hex() function

    def get_account_public_key(self):
        """
        Returns accounts public key
        :return: public key
        """
        priv_key = keys.PrivateKey(self.account.privateKey)
        pub_key = priv_key.public_key
        return pub_key.to_hex()

    def get_account_address(self):
        """
        Returns account address
        :return: address
        """
        return self.account.address
