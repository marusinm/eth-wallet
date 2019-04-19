import click
from eth_wallet.cli.new_wallet import (
    new_wallet,
)
from eth_wallet.cli.get_wallet import (
    get_wallet,
)
from eth_wallet.cli.reveal_seed import (
    reveal_seed
)
from eth_wallet.cli.get_balance import (
    get_balance,
)


@click.group()
def eth_wallet_cli():
    pass


eth_wallet_cli.add_command(new_wallet)
eth_wallet_cli.add_command(get_wallet)
eth_wallet_cli.add_command(reveal_seed)
eth_wallet_cli.add_command(get_balance)

if __name__ == "__main__":
    eth_wallet_cli()
