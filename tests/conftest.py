from eth_wallet.configuration import (
    Configuration,
)


def prepare_conf(tmp_path):
    """
    Prepare configuration file for tests
    :param tmp_path: pytest tmp_path fixture
    :return: configuration for tests
    """
    test_config = dict(
        keystore_location=str(tmp_path),
        keystore_filename='/keystore',
        eth_address='',
        public_key='',
        network=3,
    )
    test_config = Configuration(
        config_dir=str(tmp_path),
        initial_config=test_config
    )
    return test_config.load_configuration()
