import click
import getpass
from eth_wallet.cli.utils_cli import (
    get_api,
)
from eth_wallet.configuration import (
    Configuration,
)


@click.command()
@click.option('-m', '--mnemonic-sentence', default='', prompt='Mnemonic sentence',
              help='Remembered mnemonic sentence to restore wallet.')
def restore_wallet(mnemonic_sentence):
    """Creates new wallet and store encrypted keystore file."""
    passphrase = getpass.getpass('Passphrase: ')  # Prompt the user for a password of keystore file

    configuration = Configuration().load_configuration()

    api = get_api()
    wallet = api.restore_wallet(configuration, mnemonic_sentence, passphrase)

    click.echo('Account address: %s' % str(wallet.get_address()))
    click.echo('Account pub key: %s' % str(wallet.get_public_key()))
    click.echo('Keystore path: %s' % configuration.keystore_location + configuration.keystore_filename)
    click.echo('Remember these words to restore eth-wallet: %s' % wallet.get_mnemonic())




