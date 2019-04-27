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
from eth_wallet.cli.send_transaction import (
    send_transaction,
)
from eth_wallet.cli.restore_wallet import (
    restore_wallet,
)


@click.group()
def eth_wallet_cli():
    pass


eth_wallet_cli.add_command(new_wallet)
eth_wallet_cli.add_command(get_wallet)
eth_wallet_cli.add_command(reveal_seed)
eth_wallet_cli.add_command(get_balance)
eth_wallet_cli.add_command(send_transaction)
eth_wallet_cli.add_command(restore_wallet)

if __name__ == "__main__":
    eth_wallet_cli()
