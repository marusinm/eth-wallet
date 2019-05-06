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


def test_invalid_address(config):
    result = call_eth_wallet(eth_wallet_cli, parameters=["send-transaction",
                                                         "--to", "this-is-invalid-address",
                                                         "--value", "1"])
    assert result.exit_code == 0
    assert f"Invalid recipient(to) address!" in result.output


def test_invalid_vlue(config):
    result = call_eth_wallet(eth_wallet_cli, parameters=["send-transaction",
                                                         "--to", "0xfe7eaD4D9beD0F1AC2b9f7d8910d8717b505Db4c",
                                                         "--value", "this-is-invalid-value"])
    assert result.exit_code == 0
    assert f"Invalid value to send!" in result.output


def test_incorrect_password(config, mocker):
    mocker.patch('getpass.getpass',
                 return_value="incorrect-password")
    result = call_eth_wallet(eth_wallet_cli, parameters=["send-transaction",
                                                         "--to", "0xfe7eaD4D9beD0F1AC2b9f7d8910d8717b505Db4c",
                                                         "--value", "0.1"])
    assert result.exit_code == 0
    assert f"Incorrect password!" in result.output


def test_insufficient_funds(config):
    result = call_eth_wallet(eth_wallet_cli, parameters=["send-transaction",
                                                         "--to", "0xfe7eaD4D9beD0F1AC2b9f7d8910d8717b505Db4c",
                                                         "--value", "0.1"])
    assert result.exit_code == 0
    assert f"Insufficient ETH funds! Check balance on your address." in result.output


def test_unknown_token(config):
    result = call_eth_wallet(eth_wallet_cli, parameters=["send-transaction",
                                                         "--to", "0xfe7eaD4D9beD0F1AC2b9f7d8910d8717b505Db4c",
                                                         "--value", "0.1",
                                                         "--token", "invalid-token"])
    assert result.exit_code == 0
    assert f"This token is not added to the wallet!" in result.output



