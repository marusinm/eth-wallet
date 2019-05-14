from tkinter import(
    Tk,
    Frame,
    Label,
    Button,
    Entry,
    Message,
    CENTER,
    Menu,
    Menubutton,
    IntVar,
    StringVar,
    RAISED,
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

        lbl_pswd = Label(self,
                         text='Passphrase:',
                         width=60,
                         font=(None, 20))
        lbl_pswd.pack()

        entry_password = Entry(self,
                               show="*",
                               font=(None, 20),
                               justify=CENTER)
        entry_password.pack()

        btn_create_wallet = Button(self,
                                   text="Generate",
                                   width=60,
                                   font=(None, 16),
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

        lbl_remember_words = Label(self,
                                   text='Restore sentence:',
                                   width=60)
        lbl_remember_words.pack()

        lbl_mnemonic = Message(self,
                               text=self.wallet.get_mnemonic(),
                               justify=CENTER,
                               borderwidth=10,
                               background='light blue')
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
        self.tokens = self.api.list_tokens(self.configuration)
        self.eth_balance, _ = self.api.get_balance(self.configuration)

        def refresh():
            self.show()

        def change_token(token):
            if token == 'ETH':
                self.eth_balance, _ = self.api.get_balance(self.configuration)
            else:
                self.eth_balance, _ = self.api.get_balance(self.configuration, token)

            balance.set(str(self.eth_balance) + ' ' + token)

        def add_token():
            print("add token")

        token_symbol = StringVar()
        token_symbol.set('ETH')
        balance = StringVar()
        balance.set(str(self.eth_balance) + ' ' + token_symbol.get())

        mb = Menubutton(self,
                        width=60,
                        textvariable=token_symbol,
                        relief=RAISED)
        mb.grid()
        mb.menu = Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        mb.menu.add_radiobutton(label="ETH",
                                variable=token_symbol,
                                value='ETH',
                                command=lambda: change_token(token_symbol.get()))
        for token in self.tokens:
            mb.menu.add_radiobutton(label=token,
                                    variable=token_symbol,
                                    value=token,
                                    command=lambda: change_token(token_symbol.get()))
        mb.menu.add_radiobutton(label="Add new token ...",
                                command=add_token)
        mb.pack()

        label = Label(self,
                      # text=str(eth_balance) + ' ' + token_symbol.get(),
                      textvariable=balance,
                      width=60,
                      font=(None, 30))
        label.pack()

        btn_refresh = Button(self,
                             text="Refresh",
                             command=refresh,
                             width=60,
                             font=(None, 16))
        btn_refresh.pack()

        btn_send_transaction = Button(self,
                                      text="Send Transaction",
                                      command=self.show_transaction_page,
                                      width=60,
                                      font=(None, 16))
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
    root.title("Ethereum wallet")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("300x400")
    root.mainloop()
