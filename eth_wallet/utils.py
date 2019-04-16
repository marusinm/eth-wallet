from eth_utils import (
    keccak,
)


def public_key_to_keccak256(public_key_bytes: bytes) -> bytes:
    return keccak(public_key_bytes)


def public_key_bytes_to_address(public_key_bytes: bytes) -> bytes:
    return keccak(public_key_bytes)[-20:]
