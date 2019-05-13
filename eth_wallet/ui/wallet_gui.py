from tkinter import (
    Tk,
    Entry,
    Label,
    Button,
    Frame
)
from eth_wallet.configuration import (
    Configuration,
)
from eth_wallet.api import (
    WalletAPI,
)


class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Ethereum wallet")

        self.configuration = Configuration()
        self.api = WalletAPI()
        self.wallet = None

        if self.configuration.is_configuration():
            self.configuration = Configuration().load_configuration()
            self.draw_main_frame()
        else:
            self.draw_new_wallet_frame()

    def draw_main_frame(self, previous_frame=None):
        """
        Draw main wallet window
        :return:
        """
        if previous_frame is not None:
            previous_frame.pack_forget()

        frame = Frame(self.master)
        frame.pack()

        def refresh():
            self.draw_main_frame(frame)

        eth_balance, address = self.api.get_balance(self.configuration)
        label = Label(frame, text=str(eth_balance)+'ETH')
        label.pack()

        btn_refresh = Button(frame, text="Refresh", command=refresh)
        btn_refresh.pack()

    def draw_new_wallet_frame(self):
        """
        Draw frame for where user can create new wallet
        :return:
        """
        login_frame = Frame(self.master)
        login_frame.pack()

        entry_password = Entry(login_frame, show="*")
        entry_password.pack()

        btn_create_wallet = Button(login_frame,
                                   text="Generate",
                                   command=lambda: self.create_wallet(login_frame,
                                                                      btn_create_wallet,
                                                                      entry_password.get()))
        btn_create_wallet.pack()

    def create_wallet(self, login_frame, btn_create_wallet, password):
        """
        Create new wallet
        :param login_frame: login frame
        :param btn_create_wallet: only btn on login frame
        :param password: passphrase from the user
        :return:
        """
        self.configuration = Configuration().load_configuration()
        self.wallet = self.api.new_wallet(self.configuration, password)

        lbl_mnemonic = Label(login_frame, text=self.wallet.get_mnemonic())
        lbl_mnemonic.pack()
        btn_create_wallet.configure(text="Continue",
                                    command=lambda: self.draw_main_frame(previous_frame=login_frame))


if __name__ == "__main__":
    root = Tk()
    root.geometry("500x500")
    my_gui = GUI(root)
    root.mainloop()
