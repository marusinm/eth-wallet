import json
from eth_account import (
    Account,
)
from eth_keys import (
    keys,
)
from eth_wallet.utils import (
    create_directory,
)
from eth_wallet.infura import (
    Infura,
)
from eth_wallet.exceptions import (
    InvalidPasswordException,
)


class Wallet:
    """
    Class defining the main wallet account
    """

    def __init__(self, configuration):
        self.conf = configuration
        self.account = None
        self.w3 = None

    def create(self, extra_entropy=''):
        """
        Creates new wallet that means private key with an attached address using os.urandom CSPRNG
        :param extra_entropy: Add extra randomness to whatever randomness your OS can provide
        :return: object with private key
        """
        self.account = Account.create(extra_entropy)
        # update config address
        self.conf.update_eth_address(self.account.address)
        # update config public key
        priv_key = keys.PrivateKey(self.account.privateKey)
        pub_key = priv_key.public_key
        self.conf.update_public_key(pub_key.to_hex())

        self.w3 = Infura().get_web3()
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

    def save_keystore(self, password):
        """
        Encrypts and save keystore to path
        :param password: user password from keystore
        :return: path
        """
        create_directory(self.conf.keystore_location)
        keystore_path = self.conf.keystore_location + self.conf.keystore_filename
        encrypted_private_key = Account.encrypt(self.account.privateKey, password)
        with open(keystore_path, 'w+') as outfile:
            json.dump(encrypted_private_key, outfile, ensure_ascii=False)
        return keystore_path

    def load_keystore(self, password):
        """
        Loads wallet account from decrypted keystore
        :param password: user password from keystore
        :return: instance of this class
        """
        keystore_path = self.conf.keystore_location + self.conf.keystore_filename
        with open(keystore_path) as keystore:
            keyfile_json = json.load(keystore)

        try:
            private_key = Account.decrypt(keyfile_json, password)
        except ValueError:
            raise InvalidPasswordException()

        self.set_account(private_key)
        return self

    def get_private_key(self):
        """
        Returns wallet private key
        :return: private key
        """
        return self.account.privateKey  # to print private key in hex use account.privateKey.hex() function

    def get_public_key(self):
        """
        Returns wallet public key
        :return: public key
        """
        return self.conf.public_key

    def get_address(self):
        """
        Returns wallet address
        :return: address
        """
        return self.conf.eth_address

    def get_balance(self, address):
        """
        Read balance from the Ethereum network in ether
        :return: number of ether on users account
        """
        self.w3 = Infura().get_web3()
        eth_balance = self.w3.fromWei(self.w3.eth.getBalance(address), 'ether')
        return eth_balance

