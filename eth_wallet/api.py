from eth_wallet.wallet import (
    Wallet
)


class WalletAPI:

    @staticmethod
    def new_account(keystore_password, extra_entropy='', keystore_path=None):
        """
        Create new wallet account and save encrypted keystore
        :param keystore_password: user password from keystore
        :param extra_entropy: extra string entropy for CSPRNG of private key
        :param keystore_path: where to save encrypted keystore
        :return: created wallet account object and saved keystore path
        """
        wallet = Wallet()
        account = wallet.create_account(extra_entropy)

        if keystore_path is None:
            keystore_path = wallet.save_account_keystore(keystore_password)
        else:
            keystore_path = wallet.save_account_keystore(keystore_password, keystore_path)

        return account, keystore_path

    @staticmethod
    def get_account(keystore_password, keystore_path=None):
        """
        Get wallet account from default keystore location
        :param keystore_password: user password from keystore
        :param keystore_path: where to finde encrypted keystore
        :return: account object
        """
        if keystore_path is None:
            wallet = Wallet().load_account_keystore(keystore_password)
        else:
            wallet = Wallet().load_account_keystore(keystore_password, keystore_path)

        return wallet
