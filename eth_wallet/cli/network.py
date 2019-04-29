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
    network = api.get_network(configuration)
    if network == 1:
        click.echo('You are connected to the Mainnet network!')
    if network == 3:
        click.echo('You are connected to the Ropsten network!')



