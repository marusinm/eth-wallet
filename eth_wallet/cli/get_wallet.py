import click
from eth_wallet.cli.utils_cli import (
    get_api,
)
from eth_wallet.configuration import (
    Configuration,
)


@click.command()
def get_wallet():
    """Get wallet account from encrypted keystore."""
    configuration = Configuration().load_configuration()
    api = get_api()

    address, pub_key = api.get_wallet(configuration)

    click.echo('Account address: %s' % str(address))
    click.echo('Account pub key: %s' % str(pub_key))

