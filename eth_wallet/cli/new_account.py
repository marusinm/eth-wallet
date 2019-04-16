import click
import getpass
from eth_wallet.cli.utils_cli import (
    get_api,
)


@click.command()
@click.option('-e', '--extra-entropy', default='', prompt='Extra entropy',
              help='Adds extra entropy to generated private key.')
@click.option('-p', '--path', help='Path where to store keystore.')
def new_account(extra_entropy, path):
    """Creates new account and store encrypted keystore file."""
    password = getpass.getpass('Password from keystore: ')  # Prompt the user for a password of keystore file

    api = get_api()
    if path is None:
        wallet, keystore_path = api.new_account(password, extra_entropy=extra_entropy)
    else:
        wallet, keystore_path = api.new_account(password, extra_entropy=extra_entropy, keystore_path=path)

    click.echo('Account address: %s' % str(wallet.get_account_address()))
    click.echo('Account pub key: %s' % str(wallet.get_account_public_key()))
    click.echo('Keystore path: %s' % keystore_path)




