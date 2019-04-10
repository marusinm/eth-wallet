from eth_wallet.wallet import (
    Wallet
)


class WalletAPI:

    def __init__(self):
        self.wallet = Wallet()

    def new_account(self, extra_entropy=''):
        return self.wallet.create(extra_entropy)
