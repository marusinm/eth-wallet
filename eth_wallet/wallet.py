from eth_wallet.account import (
    WalletAccount,
)


class Wallet:
    """
    Class defining the main wallet functions
    """
    def __init__(self):
        self.account = WalletAccount()

    def create(self, extra_entropy=''):
        """
        Creates new wallet account
        :param extra_entropy: Add extra randomness to whatever randomness your OS can provide
        :return: object of WalletAccount
        """
        self.account.create(extra_entropy)
        return self.account

    def get_account(self):
        return self.account


# def main():
#     wallet = EthWallet()
#     wallet.create('My extra entropy')  # TODO: change to user input
#     wallet.get_account().print_private_key()
#     wallet.get_account().print_public_key()
#     wallet.get_account().print_address()


# if __name__ == '__main__':
#     main()
