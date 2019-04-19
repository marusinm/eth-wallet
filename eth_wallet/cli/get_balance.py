import click
from eth_wallet.cli.utils_cli import (
    get_api,
)
from eth_wallet.configuration import (
    Configuration,
)


@click.command()
@click.option('-a', '--address', default='', prompt='Ethereum address',
              help='Get balance of this address.')
def get_balance(address):
    """Get address balance."""
    configuration = Configuration().load_configuration()
    api = get_api()
    eth_balance = api.get_balance(configuration, address)
    print(address, eth_balance)
    click.echo('Balance on address %s is: %s' % (address, eth_balance))

