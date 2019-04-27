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
from mnemonic import (
    Mnemonic
)


class Wallet:
    """
    Class defining the main wallet account
    """

    def __init__(self, configuration):
        self.conf = configuration
        self.account = None
        self.w3 = None
        self.mnemonic_sentence = None

    def create(self, password='', restore_sentence=None):
        """
        Creates new wallet that means private key with an attached address using os.urandom CSPRNG
        :param password: Is used as extra randomness to whatever randomness your OS can provide
        :param restore_sentence: Used in case of restoring wallet from mnemonic sentence.
        :return: object with private key
        """
        extra_entropy = password

        mnemonic = Mnemonic("english")
        if restore_sentence is None:
            self.mnemonic_sentence = mnemonic.generate()
        else:
            self.mnemonic_sentence = restore_sentence

        seed = mnemonic.to_seed(self.mnemonic_sentence, extra_entropy)
        master_private_key = seed[32:]

        # self.account = Account.create(extra_entropy)
        self.account = self.set_account(master_private_key)

        # update config address
        self.conf.update_eth_address(self.account.address)
        # update config public key
        priv_key = keys.PrivateKey(self.account.privateKey)
        pub_key = priv_key.public_key
        self.conf.update_public_key(pub_key.to_hex())

        self.w3 = Infura().get_web3()
        return self

    def restore(self, mnemonic_sentence, password):
        """
        Recreates wallet from mnemonic sentence
        :param mnemonic_sentence: remembered user mnemonic sentence
        :type mnemonic_sentence: str
        :param password: password from keystore which is used as entropy too
        :return: wallet
        """
        return self.create(password, mnemonic_sentence)

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

    def get_mnemonic(self):
        """
        Returns BIP39 mnemonic sentence
        :return: mnemonic words
        """
        return self.mnemonic_sentence

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

