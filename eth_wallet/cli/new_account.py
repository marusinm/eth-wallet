import click
from eth_wallet.cli.utils_cli import (
    get_api,
)
from eth_utils import (
    decode_hex,
)


@click.command()
@click.option('-e', '--extra-entropy', default='', prompt='extra entropy',
              help='creates new account with optional entropy')
def new_account(extra_entropy):
    """Creates new account. And save it."""
    if extra_entropy != '':
        click.echo('Your extra entropy is %s!' % extra_entropy)
    api = get_api()
    account = api.new_account(extra_entropy)
    click.echo('Account address: %s' % str(account.get_account_address()))
    address_bytes = decode_hex(account.get_account_address())
    click.echo('Public key length: %d' % len(address_bytes))
    click.echo('\n')

    click.echo('Account pub key: %s' % str(account.get_account_public_key()))
    public_key_bytes = decode_hex(account.get_account_public_key())
    click.echo('Public key length: %d' % len(public_key_bytes))
    click.echo('\n')

    click.echo('Account prv key: %s' % str(account.get_account_private_key().hex()))
    click.echo('Private key length: %d' % len(account.get_account_private_key()))
    click.echo('\n')
    # TODO: save encrypted file
