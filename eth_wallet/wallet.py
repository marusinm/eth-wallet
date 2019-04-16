import json
import os
from eth_account import (
    Account,
)
from eth_keys import (
    keys,
)
from eth_wallet.utils import (
    create_directory,
)


class Wallet:
    """
    Class defining the main wallet account
    """
    # By default user’s home location ./eth-wallet directory is where to save keystore
    KEYSTORE_DIR = os.path.expanduser('~') + '/.eth-wallet'
    KEYSTORE_FILE = '/keystore'

    def __init__(self):
        self.account = None

    def create_account(self, extra_entropy=''):
        """
        Creates new account that means private key with an attached address using os.urandom CSPRNG
        :param extra_entropy: Add extra randomness to whatever randomness your OS can provide
        :return: object with private key
        """
        self.account = Account.create(extra_entropy)
        return self

    def get_account(self):
        """
        Returns account
        :return: account object
        """
        return self.account

    def set_account(self, private_key):
        """
        Creates new account from private key with appropriate address
        :param private_key: in format hex str/bytes/int/eth_keys.datatypes.PrivateKey
        :return: currently created account
        """
        self.account = Account.privateKeyToAccount(private_key)
        return self.account

    def save_account_keystore(self, password, dir_path=KEYSTORE_DIR):
        """
        Encrypts and save keystore to path
        :param password: user password from keystore
        :param dir_path: directory where to store keystore
        :return: path
        """
        create_directory(dir_path)
        encrypted_private_key = Account.encrypt(self.account.privateKey, password)
        with open(dir_path + self.KEYSTORE_FILE, 'w+') as outfile:
            json.dump(encrypted_private_key, outfile, ensure_ascii=False)
        return dir_path + self.KEYSTORE_FILE

    def load_account_keystore(self, password, dir_path=KEYSTORE_DIR):
        """
        Loads wallet account from decrypted keystore
        :param password: user password from keystore
        :param dir_path: from where to load keystore
        :return: instance of this class
        """
        with open(dir_path + self.KEYSTORE_FILE) as keystore:
            keyfile_json = json.load(keystore)

        private_key = Account.decrypt(keyfile_json, password)
        self.set_account(private_key)
        return self

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
