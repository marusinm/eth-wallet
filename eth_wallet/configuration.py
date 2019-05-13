import os
import yaml
from eth_wallet.utils import (
    create_directory,
    is_file,
)


class Configuration:
    """
    Module for working with configuration file.
    """
    # Networks defined in https://github.com/ethereum/EIPs/blob/master/EIPS/eip-155.md#specification
    MAIN_NETWORK_ID = 1
    ROPSTEN_NETWORK_ID = 3

    # By default user’s home location ./eth-wallet directory is where to save config file
    config_dir = os.path.expanduser('~') + '/.eth-wallet'
    config_file = '/config.yaml'
    # Default configuration yaml file will be created from this dictionary
    initial_config = dict(
        keystore_location=config_dir,
        keystore_filename='/keystore',
        eth_address='',
        public_key='',
        network=ROPSTEN_NETWORK_ID,  # default network where to connect app
        contracts=dict(),
    )

    def __init__(self,
                 config_dir=config_dir,
                 config_file=config_file,
                 initial_config=initial_config):

        # default class paths can be override in test within constructor
        self.config_dir = config_dir
        self.config_file = config_file
        self.config_path = config_dir + config_file
        self.initial_config = initial_config

        # Variables from configuration file. They will be initialized after load_configuration() call
        self.network = ''
        self.keystore_location = ''
        self.keystore_filename = ''
        self.eth_address = ''
        self.public_key = ''
        self.contracts = dict()

    def is_configuration(self):
        """Checks if exists configuration on default path"""
        if is_file(self.config_path):
            return True
        else:
            return False

    def load_configuration(self):
        """Load bot configuration from .yaml file"""
        if not is_file(self.config_path):
            self.create_empty_configuration()
            self.load_configuration()
        else:
            with open(self.config_path, 'r') as yaml_file:
                file = yaml.safe_load(yaml_file)
            for key, value in file.items():
                setattr(self, key, value)
        return self

    def create_empty_configuration(self):
        """
        Creates and initialize empty configuration file
        :return: True if config file created successfully
        """
        create_directory(self.config_dir)
        with open(self.config_path, 'w+') as yaml_file:
            yaml.dump(self.initial_config, yaml_file, default_flow_style=False)

        return True

    def update_eth_address(self, eth_address):
        """
        Update and save eth address to configuration
        :param eth_address: eth address to save
        :return:
        """
        self.eth_address = eth_address
        self.__update_configuration('eth_address', eth_address)

    def update_public_key(self, public_key):
        """
        Update and save public key to configuration
        :param public_key: public key to save
        :return:
        """
        self.public_key = public_key
        self.__update_configuration('public_key', public_key)

    def add_contract_token(self, contract_symbol, contract_address):
        """
        Add ERC20 token to the wallet
        :param contract_symbol: token symbol
        :param contract_address: contract address
        :return:
        """
        self.contracts[contract_symbol] = contract_address
        self.__update_configuration('contracts', self.contracts)

    def __update_configuration(self, parameter_name, parameter_value):
        """
        Updates configuration file.
        :param parameter_name: parameter name to change or append
        :param parameter_value: value to parameter_key
        :return: True if config file updated successfully
        """
        with open(self.config_path, 'r') as yaml_file:
            file = yaml.safe_load(yaml_file)

        file[parameter_name] = parameter_value

        create_directory(self.config_dir)
        with open(self.config_path, 'w+') as yaml_file:
            yaml.dump(file, yaml_file, default_flow_style=False)

        return True
