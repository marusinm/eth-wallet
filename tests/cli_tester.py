from eth_wallet.cli.eth_wallet_cli import(
    eth_wallet_cli,
)
from click.testing import(
    CliRunner,
)


def call_eth_wallet(fnc=None, parameters=None, envs=None):
    """
    Creates testing environment for cli application
    :param fnc: command to run
    :param parameters: program cmd argument
    :param envs:
    :return: invoked cli runner
    """
    fnc = fnc or eth_wallet_cli
    runner = CliRunner()
    envs = envs or {}
    parameters = parameters or []
    # catch exceptions enables debugger
    return runner.invoke(fnc, args=parameters, env=envs, catch_exceptions=False)