from eth_account import (
    Account,
)
from eth_wallet.utils import (
    public_key_to_keccak256,
)
from eth_utils import (
    to_normalized_address,
    to_hex,
    remove_0x_prefix,
)


class Transaction:
    """Abstraction over Ethereum transaction."""

    def __init__(self, account, w3):
        self.account = account
        self.w3 = w3

    @staticmethod
    def build_transaction(to_address,
                          value,
                          gas,
                          gas_price,
                          nonce,
                          chain_id,
                          data=None
                          ):
        """Collects all necessary data to build transaction dict."""
        if data is None:  # tx dict for sending ETH
            transaction = {
                # Note that the address must be in checksum format:
                'to': to_address,
                'value': value,
                'gas': gas,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': chain_id
            }
        else:  # tx dict for sending ERC20 tokens
            transaction = {
                # Note that the address must be in checksum format:
                'to': to_address,
                'value': value,
                'gas': gas,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': chain_id,
                'data': data
            }

        return transaction

    def send_transaction(self, transaction):
        """
        Signs and send transaction
        :param transaction: transaction dict
        :return: transaction hash
        """
        print('transaction: ' + str(transaction))

        signed_tx = Account.signTransaction(transaction, self.account.privateKey)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        return tx_hash

    @staticmethod
    def get_tx_erc20_data_field(receiver, value):
        """
        When creating transaction on ERC20 contract, we need to specify data field
        within transaction dictionary. This field must be in hex format and
        call solidity 'transfer(address,uint256)' function where is defined
        token receiver and amount of tokens to send. All this values must be
        concatenated as hex string

        Example of data field value is:
        0xa9059cbb --> solidity transfer(address,uint256) function an it's keccak256 hash's first 4 bytes
        000000000000000000000000aad533eb7fe7f2657960ac7703f87e10c73ae73b --> token receiver
        0000000000000000000000000000000000000000000000000de0b6b3a7640000 --> 1 * 10**ERC20-decimals value to transfer
        concatenated together.

        Description is also available within Ethereumbook:
        https://github.com/ethereumbook/ethereumbook/blob/develop/06transactions.asciidoc#transmitting-a-data-payload-to-an-eoa-or-contract

        :param receiver: address where smart contract send data
        :param value: number of tokens to send, 1 token is often 10**18 but can depend on ERC20 decimals
        :type value: integer
        :return: hex string
        """
        # 1. create hex of called function in solidity and take first 4 bytes
        # ERC20 transfer function will always produce a9059cbb.....
        transfer_hex = public_key_to_keccak256(b'transfer(address,uint256)').hex()[:8]

        # 2. create 32 byte number (length 64)
        # consisting of zeros and normalized hex address of receiver without 0x prefix
        # example: 000000000000000000000000aad533eb7fe7f2657960ac7703f87e10c73ae73b
        receiver = remove_0x_prefix(to_normalized_address(receiver))
        receiver = '000000000000000000000000' + receiver  # 32 bytes together

        # 3. convert sending amount to hex and remove 0x prefix
        # this number must be integer and therefore smallest units of token used
        # usually it 1 token is often 10**18 but can depend on ERC20 decimals
        # example: de0b6b3a7640000 (hex of 1000000000000000000)
        value = remove_0x_prefix(to_hex(value))

        # 4. add zeros in front of sending amount of hex value. Together it must be 32 bytes (length 64)
        # example: 0000000000000000000000000000000000000000000000000de0b6b3a7640000
        zero_end_point = 64 - len(value)
        final_hex_amount = [value[x - zero_end_point] if x >= zero_end_point else 0 for x in range(0, 64)]
        final_hex_amount = ''.join(str(x) for x in final_hex_amount)  # convert list to string

        # 5. concatenate final data field
        data = '0x'+transfer_hex + receiver + final_hex_amount

        return data
