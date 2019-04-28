from eth_account import (
    Account,
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
                          chain_id=3  # chain_id=3 for Ropsten test network
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

