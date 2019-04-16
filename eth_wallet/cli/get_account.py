import click
import getpass
from eth_wallet.cli.utils_cli import (
    get_api,
)


@click.command()
@click.option('-p', '--path', help='Path from where to load keystore.')
def get_account(path):
    """Get wallet account from encrypted keystore."""
    password = getpass.getpass('Password from keystore: ')  # Prompt the user for a password of keystore file

    api = get_api()

    try:
        if path is None:
            wallet = api.get_account(password)
        else:
            wallet = api.get_account(password, keystore_path=path)

        click.echo('Account address: %s' % str(wallet.get_account_address()))
        click.echo('Account pub key: %s' % str(wallet.get_account_public_key()))

    except ValueError:
        click.echo('Incorrect password!')

