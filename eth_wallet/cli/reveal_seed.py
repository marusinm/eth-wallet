import click
import getpass
from eth_wallet.cli.utils_cli import (
    get_api,
)
from eth_wallet.configuration import (
    Configuration,
)
from eth_wallet.exceptions import (
    InvalidPasswordException,
)


@click.command()
def reveal_seed():
    """Reveals private key from encrypted keystore."""
    password = getpass.getpass('Password from keystore: ')  # Prompt the user for a password of keystore file

    configuration = Configuration().load_configuration()
    api = get_api()

    try:
        wallet = api.get_private_key(configuration, password)
        click.echo('Account prv key: %s' % str(wallet.get_private_key().hex()))

    except InvalidPasswordException:
        click.echo('Incorrect password!')
