import pytest
from eth_keys import (
    keys,
)
from eth_utils import (
    decode_hex,
)
from eth_wallet.utils import (
    public_key_to_keccak256
)
from eth_wallet.wallet import (
    Wallet
)
from web3 import(
    Web3,
)
from tests.conftest import (
    prepare_conf
)


@pytest.fixture
def configuration(tmp_path):
    return prepare_conf(tmp_path)


def test_lengths(configuration):
    wallet = Wallet(configuration)
    wallet.create('eXtR4 EntroPy Str1Ng')

    # check length of private key
    assert len(wallet.get_private_key()) == 32

    # check length of public key
    public_key_bytes = decode_hex(wallet.get_public_key())
    assert len(public_key_bytes) == 64

    # check length of address
    address_bytes = decode_hex(wallet.get_address())
    assert len(address_bytes) == 20


def test_keys():
    private_key_hex = '0xa18f998097dd14034f42dd6c4d22808e2d649fb79ff6ddba3111d0d50971841d'
    private_key_bytes = decode_hex(private_key_hex)
    private_key = keys.PrivateKey(private_key_bytes)
    public_key = private_key.public_key

    # check full keccak address
    keccak256 = public_key_to_keccak256(public_key.to_bytes())
    assert keccak256.hex() == 'a54e53712efd827be401672cfe7ead4d9bed0f1ac2b9f7d8910d8717b505db4c'
    # check pub key
    assert public_key.to_hex() == '0x797d46d4ff54c5368e2a2cf8d03fc6f058c79741a66b8ebd8a7d459d724b603' \
                                  '90d2989a6af744bd96792aae86c421fb2167bb29e66a06e31428dca96130c882b'
    # check eth address - keccak-256 hash of the hexadecimal form of a public key, then keep only the last 20 bytes
    assert public_key.to_checksum_address() == '0xfe7eaD4D9beD0F1AC2b9f7d8910d8717b505Db4c'
    assert public_key.to_address() == '0xfe7ead4d9bed0f1ac2b9f7d8910d8717b505db4c'


def test_addresses(configuration):
    wallet = Wallet(configuration)
    wallet.create('eXtR4 EntroPy Str1Ng')
    assert Web3.isAddress(wallet.get_address())
    assert Web3.isChecksumAddress(wallet.get_address())
