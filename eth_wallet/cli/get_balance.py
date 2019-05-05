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
    ERC20NotExistsException,
)


@click.command()
@click.option('-t', '--token', default=None,
              help='Token symbol.')
def get_balance(token):
    """Get address balance."""
    configuration = Configuration().load_configuration()
    api = get_api()
    try:
        if token is None:
            eth_balance, address = api.get_balance(configuration)
            click.echo('Balance on address %s is: %sETH' % (address, eth_balance))
        else:
            token_balance, address = api.get_balance(configuration, token)
            click.echo('Balance on address %s is: %s%s' % (address, token_balance, token))
    except InvalidAddress:
        click.echo('Invalid address or wallet does not exist!')
    except InfuraErrorException:
        click.echo('Wallet is not connected to Ethereum network!')
    except ERC20NotExistsException:
        click.echo('This token is not added to the wallet!')


