import os
import errno
import json
from eth_utils import (
    keccak,
)


def public_key_to_keccak256(public_key_bytes: bytes) -> bytes:
    return keccak(public_key_bytes)


def public_key_bytes_to_address(public_key_bytes: bytes) -> bytes:
    return keccak(public_key_bytes)[-20:]


def is_file(path):
    """
    Checks if path is file.
    :param path: path with filename
    :return: True if file exists
    """
    return os.path.isfile(path)


def is_directory(path):
    """
    Checks if path is directory.
    :param path: path with directory
    :return: True if is directory, False if directory doesn't exist
    """
    if os.path.exists(path):
        return True
    return False


def create_directory(dirname):
    """
    Crete directory if doesn't already exist.
    :param dirname: path with new directory
    :return: path with directory
    """
    if not is_directory(dirname):
        try:
            os.makedirs(dirname)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def get_abi_json():
    """
    Returns FITCOIN ERC20 token ABI
    :return:
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    abi_path = os.path.join(root_dir, 'erc20', 'abi.json')
    with open(abi_path) as f:
        fitcoin = json.load(f)
    return fitcoin
