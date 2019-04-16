import os
import errno
from eth_utils import (
    keccak,
)


def public_key_to_keccak256(public_key_bytes: bytes) -> bytes:
    return keccak(public_key_bytes)


def public_key_bytes_to_address(public_key_bytes: bytes) -> bytes:
    return keccak(public_key_bytes)[-20:]


def is_directory(dirname):
    """
    Checks if filename is directory.
    :param dirname: path with directory
    :return: True if is directory, False if directory doesn't exist
    """
    if os.path.exists(dirname):
        return True
    return False


def create_directory(dirname):
    """
    Crete directory.
    :param dirname: path with new directory
    :return: path with directory
    """
    if not is_directory(dirname):
        try:
            os.makedirs(dirname)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
