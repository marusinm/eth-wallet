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
from eth_wallet.cli.add_token import (
    add_token,
)
from eth_wallet.cli.list_tokens import (
    list_tokens,
)
from eth_wallet.cli.network import (
    network,
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
eth_wallet_cli.add_command(add_token)
eth_wallet_cli.add_command(list_tokens)
eth_wallet_cli.add_command(network)

if __name__ == "__main__":
    eth_wallet_cli()
