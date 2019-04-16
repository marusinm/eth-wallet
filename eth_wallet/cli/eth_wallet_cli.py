import click
from eth_wallet.cli.new_account import (
    new_account,
)


@click.group()
def eth_wallet_cli():
    pass


eth_wallet_cli.add_command(new_account)

if __name__ == "__main__":
    eth_wallet_cli()
