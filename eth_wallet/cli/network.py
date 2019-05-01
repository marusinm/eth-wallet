import click
from eth_wallet.cli.utils_cli import (
    get_api,
)
from eth_wallet.configuration import (
    Configuration,
)


@click.command()
def network():
    """Get connected network (Mainnet, Ropsten) defined in EIP155."""
    configuration = Configuration().load_configuration()
    api = get_api()
    chain_id = api.get_network(configuration)
    if chain_id == 1:
        click.echo('You are connected to the Mainnet network!')
    if chain_id == 3:
        click.echo('You are connected to the Ropsten network!')
