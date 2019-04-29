from eth_account import (
    Account,
)
from eth_wallet.utils import (
    public_key_to_keccak256,
)


class Transaction:
    """Abstraction over Ethereum transaction."""

    def __init__(self, account, w3):
        self.account = account
        self.w3 = w3

    def build_transaction(self,
                          to_address,
                          value,
                          gas,
                          gas_price,
                          nonce,
                          chain_id
                          ):
        """Collects all necessary data to build transaction dict."""
        transaction = {
            # Note that the address must be in checksum format:
            'to': to_address,
            'value': value,
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
            'chainId': chain_id
        }

        return transaction

    def build_contract_transaction(self,
                                   to_address,
                                   value,
                                   gas,
                                   gas_price,
                                   nonce,
                                   chain_id
                                   ):
        """Collects all necessary data to build transaction dict."""

        # create hex of called transaction and take first 4 bytes
        called_function_hex = public_key_to_keccak256(b'transfer(address,uint256)').hex()[:8]
        token_receiver = '000000000000000000000000'+to_address[:-40]  # add zeros and remove 0x


        transaction = {
            # Note that the address must be in checksum format:
            'to': to_address,
            'value': value,
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
            'chainId': chain_id
        }

        return transaction

    def send_transaction(self, transaction):
        """
        Signs and send transaction
        :param transaction: transaction dict
        :return: transaction hash
        """
        print('transaction: ' + str(transaction))

        signed_tx = Account.signTransaction(transaction, self.account.privateKey)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        return tx_hash
