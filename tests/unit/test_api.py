from eth_wallet.api import(
    WalletAPI,
)
from tests.conftest import (
    prepare_conf,
)
from web3 import (
    Web3,
)
from eth_utils import (
    decode_hex,
)


def test_account(tmp_path):
    test_configuration = prepare_conf(tmp_path)

    WalletAPI.new_wallet(test_configuration, 'my-password')
    assert len(list(tmp_path.iterdir())) == 2  # one config.yaml and one keystore

    address, pub_key = WalletAPI.get_wallet(test_configuration)
    public_key_bytes = decode_hex(pub_key)
    assert len(public_key_bytes) == 64
    assert Web3.isAddress(address)
    assert Web3.isChecksumAddress(address)
