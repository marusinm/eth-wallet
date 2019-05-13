from eth_wallet.ui.page import (
    Page,
)
from tkinter import (
    Label,
    Entry,
    Button
)
from eth_wallet.configuration import (
    Configuration,
)
from eth_wallet.api import (
    WalletAPI,
)
from eth_wallet.ui.home_page import (
    HomePage
)


class NewWallet(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.configuration = None
        self.api = WalletAPI()
        self.wallet = None

        entry_password = Entry(self, show="*")
        entry_password.pack()

        btn_create_wallet = Button(self,
                                   text="Generate",
                                   command=lambda: self.create_wallet(btn_create_wallet,
                                                                      entry_password.get()))

        btn_create_wallet.pack()

    def create_wallet(self, btn_create_wallet, password):
        """
        Create new wallet
        :param btn_create_wallet: generate button which change text and functionality
        :param password: passphrase from the user
        :return:
        """
        self.configuration = Configuration().load_configuration()
        self.wallet = self.api.new_wallet(self.configuration, password)

        lbl_mnemonic = Label(self, text=self.wallet.get_mnemonic())
        lbl_mnemonic.pack()
        btn_create_wallet.configure(text="Continue",
                                    command=self.show_home_page)

    def show_home_page(self):
        """
        Show home page
        :return:
        """
        info_page = HomePage(self)
        info_page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        info_page.show()

