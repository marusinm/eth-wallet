import pytest
from tests.conftest import (
    prepare_conf,
)
from tests.cli_tester import (
    call_eth_wallet,
)
from eth_wallet.cli.eth_wallet_cli import(
    eth_wallet_cli,
)


@pytest.fixture
def config(tmp_path, mocker):
    test_configuration = prepare_conf(tmp_path)
    mocker.patch('eth_wallet.configuration.Configuration.load_configuration',
                 return_value=test_configuration)
    mocker.patch('getpass.getpass',
                 return_value="my-password")
    call_eth_wallet(eth_wallet_cli, parameters=["new-wallet"])
    return test_configuration


def test_get_wallet(config):
    result = call_eth_wallet(eth_wallet_cli, parameters=["get-wallet"])
    address = config.eth_address
    pub_key = config.public_key
    assert result.exit_code == 0
    assert f"Account address: " + address + "\n" in result.output
    assert f"Account pub key: " + pub_key + "\n" in result.output

