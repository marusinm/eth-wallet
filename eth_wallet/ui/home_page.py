from eth_wallet.ui.page import (
    Page,
)
from tkinter import (
    Label,
    Button,
)
from eth_wallet.api import (
    WalletAPI,
)
from eth_wallet.configuration import (
    Configuration,
)


class HomePage(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # label = Label(self, text="This is home page")
        # label.pack(side="top", fill="both", expand=True)
        self.configuration = Configuration().load_configuration()
        self.api = WalletAPI()
        self.wallet = None

        def refresh():
            self.show()

        eth_balance, address = self.api.get_balance(self.configuration)
        label = Label(self, text=str(eth_balance)+'ETH')
        label.pack()

        btn_refresh = Button(self, text="Refresh", command=refresh)
        btn_refresh.pack()
