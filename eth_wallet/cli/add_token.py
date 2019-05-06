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
@click.option('-c', '--contract', default='', prompt='Contract address',
              help='Contract address.')
@click.option('-s', '--symbol', default='', prompt='Token symbol',
              help='Token symbol.')
def add_token(contract, symbol):
    """Add new ERC20 contract."""
    configuration = Configuration().load_configuration()
    api = get_api()

    # fitcoin_address = '0x19896cB57Bc5B4cb92dbC7D389DBa6290AF505Ce'
    try:
        api.add_contract(configuration, symbol, contract)
        click.echo('New coin was added! %s %s' % (symbol, contract))
    except InvalidAddress:
        click.echo('Invalid address or wallet does not exist!')
    except InfuraErrorException:
        click.echo('Wallet is not connected to Ethereum network!')


