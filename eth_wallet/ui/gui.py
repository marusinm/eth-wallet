from tkinter import(
    Tk,
    Frame,
)
from eth_wallet.ui.new_wallet import (
    NewWallet
)
from eth_wallet.ui.home_page import (
    HomePage
)
from eth_wallet.configuration import (
    Configuration,
)
from eth_wallet.api import (
    WalletAPI,
)


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.configuration = Configuration()
        self.api = WalletAPI()
        self.wallet = None

        if self.configuration.is_configuration():
            screen = HomePage(self)
        else:
            screen = NewWallet(self)

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
