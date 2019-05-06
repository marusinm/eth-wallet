from eth_wallet.utils import (
    get_abi_json,
    create_directory,
)


def test_create_dictionary(tmp_path):
    create_directory(str(tmp_path)+'/test')
    assert len(list(tmp_path.iterdir())) == 1


def test_abi_json():
    erc20_abi = get_abi_json()
    assert isinstance(erc20_abi, list)
    assert isinstance(erc20_abi[0], dict)

