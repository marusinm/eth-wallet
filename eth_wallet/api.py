from web3 import Web3
import time
from eth_wallet.wallet import (
    Wallet
)
from eth_wallet.transaction import (
    Transaction,
)
from eth_wallet.infura import (
    Infura,
)
from eth_wallet.exceptions import (
    InsufficientFundsException,
    InvalidValueException,
)
from web3.exceptions import (
    InvalidAddress,
)
from decimal import (
    Decimal,
)


class WalletAPI:

    @staticmethod
    def new_wallet(configuration, password):
        """
        Create new wallet account and save encrypted keystore
        :param configuration: loaded configuration file instance
        :param password: set password from keystore and used also as entropy for CSPRNG
        :return: created wallet object and saved keystore path
        """
        wallet = Wallet(configuration).create(password)
        wallet.save_keystore(password)

        return wallet

    @staticmethod
    def restore_wallet(configuration, mnemonic_sentence, passphrase):
        """
        Create new wallet account and save encrypted keystore
        :param configuration: loaded configuration file instance
        :param mnemonic_sentence: user's mnemonic sentence to restore wallet
        :param password: set password from keystore and used also as entropy for CSPRNG
        :return: restored wallet object and saved keystore path
        """
        wallet = Wallet(configuration).restore(mnemonic_sentence, passphrase)
        wallet.save_keystore(passphrase)

        return wallet

    @staticmethod
    def get_private_key(configuration, keystore_password):
        """
        Get account private key from default keystore location
        :param configuration: loaded configuration file instance
        :param keystore_password: user password from keystore
        :return: account object
        """
        wallet = Wallet(configuration).load_keystore(keystore_password)

        return wallet

    @staticmethod
    def get_wallet(configuration):
        """
        Get account address and private key from default keystore location
        :param configuration: loaded configuration file instance
        :return: account object
        """
        address = Wallet(configuration).get_address()
        pub_key = Wallet(configuration).get_public_key()

        return address, pub_key

    @staticmethod
    def get_balance(configuration):
        """
        Get balance from account address.
        :param configuration: loaded configuration file instance
        :return:
        """
        address = Wallet(configuration).get_address()
        eth_balance = Wallet(configuration).get_balance(address)
        return eth_balance, address

    @staticmethod
    def send_transaction(configuration,
                         keystore_password,
                         to_address,
                         eth_value):
        """
        Sign and send transaction
        :param configuration: loaded configuration file instance
        :param keystore_password: password from encrypted keystore with private key for transaction sign
        :param to_address: address in hex string where originator's funds will be sent
        :param eth_value: amount of funds to send in ETH
        :return: tuple of transaction hash and transaction cost
        """
        # this wallet address: 0x36De5DCb6461F67F4fb742D494F38eeE87316655
        # my metamask address: 0xAAD533eb7Fe7F2657960AC7703F87E10c73ae73b
        # my metamask address: 0xaad533eb7fe7f2657960ac7703f87e10c73ae73b
        # current transaction fee is: 0.000021ETH
        wallet = Wallet(configuration).load_keystore(keystore_password)
        w3 = Infura().get_web3()
        transaction = Transaction(
            account=wallet.get_account(),
            w3=w3
        )

        # check if value to send is possible to convert number
        try:
            float(eth_value)
        except ValueError:
            raise InvalidValueException()

        # create transaction dict
        tx_dict = transaction.build_transaction(
            to_address=to_address,
            value=Web3.toWei(eth_value, "ether"),
            gas=21000,  # fixed gasLimit to transfer ether from one EOA to another EOA (doesn't include contracts)
            gas_price=w3.eth.gasPrice,
            # be careful about sending too much transactions in row, nonce will be duplicated
            nonce=w3.eth.getTransactionCount(wallet.get_address())
        )

        # check whether to address is valid checksum address
        if not Web3.isChecksumAddress(to_address):
            raise InvalidAddress()

        # check whether there is sufficient balance for this transaction
        balance, _ = WalletAPI.get_balance(configuration)
        transaction_const_wei = tx_dict['gas'] * tx_dict['gasPrice']
        transaction_const_eth = w3.fromWei(transaction_const_wei, 'ether')
        if (transaction_const_eth + Decimal(eth_value)) > balance:
            raise InsufficientFundsException()

        # send transaction
        tx_hash = transaction.send_transaction(tx_dict)

        print('Pending', end='', flush=True)
        while True:
            tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
            if tx_receipt is None:
                print('.', end='', flush=True)
                time.sleep(1)
            else:
                print('\nTransaction mined!')
                break

        return tx_hash, transaction_const_eth

