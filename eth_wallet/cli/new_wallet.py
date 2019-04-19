import click
import getpass
from eth_wallet.cli.utils_cli import (
    get_api,
)
from eth_wallet.configuration import (
    Configuration,
)


@click.command()
@click.option('-e', '--extra-entropy', default='', prompt='Extra entropy',
              help='Adds extra entropy to generated private key.')
def new_wallet(extra_entropy):
    """Creates new wallet and store encrypted keystore file."""
    password = getpass.getpass('Password from keystore: ')  # Prompt the user for a password of keystore file

    configuration = Configuration().load_configuration()

    api = get_api()
    wallet = api.new_wallet(configuration, password, extra_entropy=extra_entropy)

    click.echo('Account address: %s' % str(wallet.get_address()))
    click.echo('Account pub key: %s' % str(wallet.get_public_key()))
    click.echo('Keystore path: %s' % configuration.keystore_location + configuration.keystore_filename)




