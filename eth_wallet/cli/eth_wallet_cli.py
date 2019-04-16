import click
from eth_wallet.cli.new_account import (
    new_account,
)
from eth_wallet.cli.get_account import (
    get_account,
)
from eth_wallet.cli.reveal_private_key import (
    reveal_private_key
)


@click.group()
def eth_wallet_cli():
    pass


eth_wallet_cli.add_command(new_account)
eth_wallet_cli.add_command(get_account)
eth_wallet_cli.add_command(reveal_private_key)

if __name__ == "__main__":
    eth_wallet_cli()
