from tkinter import(
    Tk,
    Frame,
    Label,
    Button,
    Entry,
)
from eth_wallet.configuration import (
    Configuration,
)
from eth_wallet.api import (
    WalletAPI,
)
from eth_wallet.ui.page import (
    Page
)


class NewWalletPage(Page):

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


class TransactionPage(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.configuration = Configuration().load_configuration()
        self.api = WalletAPI()

        label = Label(self, text='transaction page')
        label.pack()

        btn_back = Button(self, text="Back", command=self.show_home_page)
        btn_back.pack()

    def show_home_page(self):
        """
        Show home page
        :return:
        """
        info_page = HomePage(self)
        info_page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        info_page.show()


class HomePage(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.configuration = Configuration().load_configuration()
        self.api = WalletAPI()

        def refresh():
            self.show()

        eth_balance, address = self.api.get_balance(self.configuration)
        label = Label(self, text=str(eth_balance)+'ETH')
        label.pack()

        btn_refresh = Button(self, text="Refresh", command=refresh)
        btn_refresh.pack()

        btn_send_transaction = Button(self, text="Send Transaction", command=self.show_transaction_page)
        btn_send_transaction.pack()

    def show_transaction_page(self):
        """
        Show transaction page
        :return:
        """
        transaction_page = TransactionPage(self)
        transaction_page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        transaction_page.show()


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.configuration = Configuration()
        self.api = WalletAPI()
        self.wallet = None

        if self.configuration.is_configuration():
            screen = HomePage(self)
        else:
            screen = NewWalletPage(self)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        screen.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        screen.show()


if __name__ == "__main__":
    root = Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("500x600")
    root.mainloop()
