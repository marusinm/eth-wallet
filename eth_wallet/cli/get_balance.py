import click
from eth_wallet.cli.utils_cli import (
    get_api,
)
from eth_wallet.configuration import (
    Configuration,
)
from web3.exceptions import (
    InvalidAddress,
)
from eth_wallet.exceptions import (
    InfuraErrorException,
)


@click.command()
# @click.option('-a', '--address', default='', prompt='Ethereum address',
#               help='Get balance of this address.')
def get_balance():
    """Get address balance."""
    configuration = Configuration().load_configuration()
    api = get_api()
    try:
        eth_balance, address = api.get_balance(configuration)
        click.echo('Balance on address %s is: %s' % (address, eth_balance))
    except InvalidAddress:
        click.echo('Invalid address or wallet does not exist!')
    except InfuraErrorException:
        click.echo('Wallet is not connected to Ethereum network!')


