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
    InsufficientERC20FundsException,
    ERC20NotExistsException,
)
from eth_wallet.contract import (
    Contract,
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
    def get_network(configuration):
        """
        Returns connected network (Mainnet, Ropsten ...)
        :param configuration: loaded configuration file instance
        :return: network number defined in EIP155
        """
        return configuration.network

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
    def get_balance(configuration, token_symbol=None):
        """
        Get balance from account address.
        :param configuration: loaded configuration file instance
        :param token_symbol: None for ETH, ERC20 symbol for other tokens
        :return:
        """
        wallet_address = Wallet(configuration).get_address()
        if token_symbol is None:
            balance = Wallet(configuration).get_balance(wallet_address)
        else:
            try:  # check if token is added to the wallet
                contract_address = configuration.contracts[token_symbol]
            except KeyError:
                raise ERC20NotExistsException()
            contract = Contract(configuration, contract_address)
            balance = contract.get_balance(wallet_address)
        return balance, wallet_address

    @staticmethod
    def send_transaction(configuration,
                         keystore_password,
                         to_address,
                         value,
                         token_symbol=None,
                         gas_price_speed=20  # MetaMask default transaction speedup is gasPrice*10
                         ):
        """
        Sign and send transaction
        :param configuration: loaded configuration file instance
        :param keystore_password: password from encrypted keystore with private key for transaction sign
        :param to_address: address in hex string where originator's funds will be sent
        :param value: amount of funds to send in ETH or token defined in token_symbol
        :param token_symbol: None for ETH, ERC20 symbol for other tokens transaction
        :param gas_price_speed: gas price will be multiplied with this number to speed up transaction
        :return: tuple of transaction hash and transaction cost
        """
        # my MetaMask address: 0xAAD533eb7Fe7F2657960AC7703F87E10c73ae73b
        wallet = Wallet(configuration).load_keystore(keystore_password)
        w3 = Infura().get_web3()
        transaction = Transaction(
            account=wallet.get_account(),
            w3=w3
        )

        # check if value to send is possible to convert to the number
        try:
            float(value)
        except ValueError:
            raise InvalidValueException()

        if token_symbol is None:  # create ETH transaction dictionary
            tx_dict = transaction.build_transaction(
                to_address=to_address,
                value=Web3.toWei(value, "ether"),
                gas=21000,  # fixed gasLimit to transfer ether from one EOA to another EOA (doesn't include contracts)
                gas_price=w3.eth.gasPrice * gas_price_speed,
                # be careful about sending more transactions in row, nonce will be duplicated
                nonce=w3.eth.getTransactionCount(wallet.get_address()),
                chain_id=configuration.network
            )
        else:  # create ERC20 contract transaction dictionary
            try:  # check if token is added to the wallet
                contract_address = configuration.contracts[token_symbol]
            except KeyError:
                raise ERC20NotExistsException()
            contract = Contract(configuration, contract_address)
            erc20_decimals = contract.get_decimals()
            token_amount = int(float(value) * (10 ** erc20_decimals))
            data_for_contract = Transaction.get_tx_erc20_data_field(to_address, token_amount)

            # check whether there is sufficient ERC20 token balance
            erc20_balance, _ = WalletAPI.get_balance(configuration, token_symbol)
            if float(value) > erc20_balance:
                raise InsufficientERC20FundsException()

            # calculate how much gas I need, unused gas is returned to the wallet
            estimated_gas = w3.eth.estimateGas(
                {'to': contract_address,
                 'from': wallet.get_address(),
                 'data': data_for_contract
                 })

            tx_dict = transaction.build_transaction(
                to_address=contract_address,  # receiver address is defined in data field for this contract
                value=0,  # amount of tokens to send is defined in data field for contract
                gas=estimated_gas,
                gas_price=w3.eth.gasPrice * gas_price_speed,
                # be careful about sending more transactions in row, nonce will be duplicated
                nonce=w3.eth.getTransactionCount(wallet.get_address()),
                chain_id=configuration.network,
                data=data_for_contract
            )

        # check whether to address is valid checksum address
        if not Web3.isChecksumAddress(to_address):
            raise InvalidAddress()

        # check whether there is sufficient eth balance for this transaction
        balance, _ = WalletAPI.get_balance(configuration)
        transaction_const_wei = tx_dict['gas'] * tx_dict['gasPrice']
        transaction_const_eth = w3.fromWei(transaction_const_wei, 'ether')
        if token_symbol is None:
            if (transaction_const_eth + Decimal(value)) > balance:
                raise InsufficientFundsException()
        else:
            if transaction_const_eth > balance:
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

    @staticmethod
    def add_contract(configuration, contract_symbol, contract_address):
        """
        Adds new contract ERC20 token into config file with symbol and address
        :param configuration: configuration file
        :param contract_symbol: contract symbol
        :param contract_address: contract address
        :return:
        """
        contract = Contract(configuration, contract_address)
        contract.add_new_contract(contract_symbol, contract_address)

    @staticmethod
    def list_tokens(configuration):
        """
        List all added tokens from configuration file
        :param configuration: config file
        :return: dict with tokens
        """
        return configuration.contracts

