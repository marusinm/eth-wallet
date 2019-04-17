import hexbytes
from eth_wallet.api import WalletAPI


def test_account(tmp_path):
    WalletAPI.new_account('my-password', keystore_path=str(tmp_path))
    assert len(list(tmp_path.iterdir())) == 1

    wallet = WalletAPI.get_account('my-password', keystore_path=str(tmp_path))
    assert type(wallet.get_account_private_key()) == hexbytes.main.HexBytes
