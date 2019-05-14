import threading
from tkinter import (
    Tk,
    Frame,
    Label,
    Button,
    Entry,
    Message,
    CENTER,
    Menu,
    Menubutton,
    StringVar,
    RAISED,
    messagebox,
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
                                    command=self.navigate_home_page)

    def navigate_home_page(self):
        """
        Navigate to home page
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
        self.tokens = self.api.list_tokens(self.configuration)
        self.eth_balance, _ = self.api.get_balance(self.configuration)

        def change_token(token):
            if token == 'ETH':
                self.eth_balance, _ = self.api.get_balance(self.configuration)
            else:
                self.eth_balance, _ = self.api.get_balance(self.configuration, token)

            balance.set(str(self.eth_balance) + ' ' + token)

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
        mb.pack()

        label = Label(self,
                      textvariable=balance,
                      width=60,
                      font=(None, 30))
        label.pack()

        lbl_address = Label(self,
                            text="To address:",
                            width=60,
                            font=(None, 20))
        lbl_address.pack()

        entry_address = Entry(self,
                              font=(None, 20),
                              width=60,
                              justify=CENTER)
        entry_address.pack()

        lbl_amount = Label(self,
                           text="Amount:",
                           width=60,
                           font=(None, 20))
        lbl_amount.pack()

        entry_amount = Entry(self,
                             font=(None, 20),
                             width=60,
                             justify=CENTER)
        entry_amount.pack()

        lbl_passphrase = Label(self,
                               text="Passphrase:",
                               width=60,
                               font=(None, 20))
        lbl_passphrase.pack()

        entry_passphrase = Entry(self,
                                 font=(None, 20),
                                 width=60,
                                 justify=CENTER)
        entry_passphrase.pack()

        btn_send = Button(self,
                          text="Send",
                          width=60,
                          font=(None, 16),
                          command=lambda: self.send_transaction(entry_address.get(),
                                                                entry_amount.get(),
                                                                entry_passphrase.get(),
                                                                token_symbol.get()))
        btn_send.pack()

        btn_back = Button(self,
                          text="Back",
                          width=60,
                          font=(None, 16),
                          command=self.navigate_home_page)
        btn_back.pack()

    def navigate_home_page(self):
        """
        Navigate to home page
        :return:
        """
        info_page = HomePage(self)
        info_page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        info_page.show()

    def send_transaction(self, to, value, password, token):
        """
        Send transaction
        :return:
        """
        if token == 'ETH':
            tx_thread = TransactionThread(configuration=self.configuration,
                                          password=password,
                                          to=to,
                                          value=value,
                                          token=None)
        else:
            tx_thread = TransactionThread(configuration=self.configuration,
                                          password=password,
                                          to=to,
                                          value=value,
                                          token=token)
        tx_thread.start()


class TransactionThread(threading.Thread):
    def __init__(self, configuration, password, to, value, token=None):
        threading.Thread.__init__(self)
        self.api = WalletAPI()
        self.configuration = configuration
        self.password = password
        self.to = to
        self.value = value
        self.token = token

    def run(self):
        if self.token is None:
            # send ETH transaction
            tx_hash, tx_cost_eth = self.api.send_transaction(self.configuration,
                                                             self.password,
                                                             self.to,
                                                             self.value)
        else:
            # send erc20 transaction
            tx_hash, tx_cost_eth = self.api.send_transaction(self.configuration,
                                                             self.password,
                                                             self.to,
                                                             self.value,
                                                             self.token)
        messagebox.showinfo("Transaction mined!",
                            "Transaction was mined for " + str(tx_cost_eth) + "ETH fee.")

        
class AddTokenPage(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.configuration = Configuration().load_configuration()
        self.api = WalletAPI()

        lbl_symbol = Label(self,
                           text="Contract's symbol:",
                           width=60,
                           font=(None, 20))
        lbl_symbol.pack()

        entry_symbol = Entry(self,
                             font=(None, 20),
                             width=60,
                             justify=CENTER)
        entry_symbol.pack()

        lbl_address = Label(self,
                            text="Contract's address:",
                            width=60,
                            font=(None, 20))
        lbl_address.pack()

        entry_address = Entry(self,
                              font=(None, 20),
                              width=60,
                              justify=CENTER)
        entry_address.pack()

        btn_back = Button(self,
                          text="Add",
                          font=(None, 16),
                          width=60,
                          command=lambda: self.add_token(entry_symbol.get(), entry_address.get()))
        btn_back.pack()
        btn_back = Button(self,
                          text="Back",
                          font=(None, 16),
                          width=60,
                          command=self.navigate_home_page)
        btn_back.pack()

    def navigate_home_page(self):
        """
        Navigate to home page
        :return:
        """
        info_page = HomePage(self)
        info_page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        info_page.show()
        
    def add_token(self, symbol, contract):
        """
        Add new token and navigate to home page
        :param symbol: token symbol
        :param contract: contracts address
        :return:
        """
        self.api.add_contract(self.configuration, symbol, contract)
        info_page = HomePage(self)
        info_page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        info_page.show()


class HomePage(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.configuration = Configuration().load_configuration()
        self.api = WalletAPI()
        self.tokens = self.api.list_tokens(self.configuration)
        self.eth_balance, self.address = self.api.get_balance(self.configuration)

        def refresh():
            change_token(token_symbol.get())

        def change_token(token):
            if token == 'ETH':
                self.eth_balance, self.address = self.api.get_balance(self.configuration)
            else:
                self.eth_balance, self.address = self.api.get_balance(self.configuration, token)
            balance.set(str(self.eth_balance) + ' ' + token)

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
                                command=self.navigate_add_token_page)
        mb.pack()

        label_address_lbl = Label(self,
                                  text='Address:',
                                  width=60,
                                  font=(None, 10, "bold"))
        label_address_lbl.pack()
        label_address = Label(self,
                              text=self.address,
                              width=60,
                              font=(None, 10))
        label_address.pack()

        label_balance = Label(self,
                              textvariable=balance,
                              width=60,
                              font=(None, 30))
        label_balance.pack()

        btn_refresh = Button(self,
                             text="Refresh",
                             command=refresh,
                             width=60,
                             font=(None, 16))
        btn_refresh.pack()

        btn_copy_address = Button(self,
                                  text="Copy address",
                                  command=self.copy_address,
                                  width=60,
                                  font=(None, 16))
        btn_copy_address.pack()

        btn_send_transaction = Button(self,
                                      text="Send Transaction",
                                      command=self.navigate_transaction_page,
                                      width=60,
                                      font=(None, 16))
        btn_send_transaction.pack()

    def navigate_transaction_page(self):
        """
        Navigate to transaction page
        :return:
        """
        transaction_page = TransactionPage(self)
        transaction_page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        transaction_page.show()

    def navigate_add_token_page(self):
        """
        Navigate to transaction page
        :return:
        """
        add_token_page = AddTokenPage(self)
        add_token_page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        add_token_page.show()

    def copy_address(self):
        """Add address to the clipboard"""
        self.clipboard_clear()  # clear clipboard contents
        self.clipboard_append(self.address)  # append new value to clipbao 


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
