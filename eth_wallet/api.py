from eth_wallet.wallet import (
    Wallet
)
# from eth_wallet.configuration import (
#     configuration
# )
from web3.exceptions import (
    InvalidAddress,
)


class WalletAPI:

    @staticmethod
    def new_wallet(configuration, keystore_password, extra_entropy=''):
        """
        Create new wallet account and save encrypted keystore
        :param keystore_password: user password from keystore
        :param extra_entropy: extra string entropy for CSPRNG of private key
        :return: created wallet account object and saved keystore path
        """
        wallet = Wallet(configuration).create(extra_entropy)
        wallet.save_keystore(keystore_password)

        return wallet

    @staticmethod
    def get_wallet(configuration):
        """
        Get account address and private key from default keystore location
        :return: account object
        """
        address = Wallet(configuration).get_address()
        pub_key = Wallet(configuration).get_public_key()

        return address, pub_key

    @staticmethod
    def get_balance(configuration, address):
        try:
            eth_balance = Wallet(configuration).get_balance(address)
            return eth_balance
        except InvalidAddress:
            return 'Wallet does not exist!'

    @staticmethod
    def get_private_key(configuration, keystore_password):
        """
        Get account private key from default keystore location
        :param keystore_password: user password from keystore
        :return: account object
        """
        wallet = Wallet(configuration).load_keystore(keystore_password)

        return wallet
