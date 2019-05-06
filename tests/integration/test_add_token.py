import pytest
from tests.conftest import (
    prepare_conf,
)
from tests.cli_tester import (
    call_eth_wallet,
)
from eth_wallet.cli.eth_wallet_cli import (
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


def test_add_token(config):
    result = call_eth_wallet(eth_wallet_cli, parameters=["add-token",
                                                         "--contract", "0x19896cB57Bc5B4cb92dbC7D389DBa6290AF505Ce",
                                                         "--symbol", "FIT"])
    contract_address = config.contracts['FIT']
    assert result.exit_code == 0
    assert f"New coin was added! FIT " + contract_address + "\n" in result.output

    result = call_eth_wallet(eth_wallet_cli, parameters=["list-tokens"])
    assert result.exit_code == 0
    assert f"ETH\nFIT\n" in result.output
