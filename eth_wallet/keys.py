"""
module defining private, public keys and Ethereum addresses
"""
from eth_account import (
    Account,
)
from eth_keys import (
    keys,
)
from eth_utils import (
    decode_hex,
)
from eth_wallet.utils import (
    public_key_to_keccak256
)


def create_private_key(extra_entropy=''):
    """
    Create private key with an attached address using os.urandom CSPRNG
    :param extra_entropy: Add extra randomness to whatever randomness your OS can provide
    :return: object with private key
    """
    account = Account.create(extra_entropy)
    return account


def public_key_from_private():
    #myown
    priv_key_bytes = decode_hex('0xa18f998097dd14034f42dd6c4d22808e2d649fb79ff6ddba3111d0d50971841d')
    priv_key = keys.PrivateKey(priv_key_bytes)
    pub_key = priv_key.public_key
    # check pub key
    assert pub_key.to_hex() == '0x797d46d4ff54c5368e2a2cf8d03fc6f058c79741a66b8ebd8a7d459d724b60390d2989a6af744bd96792aae86c421fb2167bb29e66a06e31428dca96130c882b'
    # check eth address - keccak-256 hash of the hexadecimal form of a public key, then keep only the last 20 bytes
    assert pub_key.to_checksum_address() == '0xfe7eaD4D9beD0F1AC2b9f7d8910d8717b505Db4c'
    assert pub_key.to_address() == '0xfe7ead4d9bed0f1ac2b9f7d8910d8717b505db4c'

    #check full keccak address
    keccak256 = public_key_to_keccak256(pub_key.to_bytes())
    assert keccak256.hex() == 'a54e53712efd827be401672cfe7ead4d9bed0f1ac2b9f7d8910d8717b505db4c'


def print_account(account):
    print('private key in bytes:' + str(account.privateKey))
    print('private key in hex:' + str(account.privateKey.hex()))

    priv_key = keys.PrivateKey(account.privateKey)
    pub_key = priv_key.public_key
    print('public key in hex:' + pub_key.to_hex())

    assert pub_key.to_checksum_address() == account.address
    print('eth address in hex:' + account.address)


public_key_from_private()
print_account(create_private_key())