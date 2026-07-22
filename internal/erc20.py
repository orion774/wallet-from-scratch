from internal.remote_procedure_call import rpc_call
from internal.utilities import decode_abi_string, keccak256

TOKEN_SYMBOL_TO_CONTRACT_ADDRESS = {
    # USDC token contract on Ethereum mainnet.
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
}

def call_erc20(
    token_contract_address: str,
    function_selector: bytes,
    function_arguments: list,
) -> str:
    call_data = function_selector + b"".join(function_arguments)

    result_hex = rpc_call(
        method="eth_call",
        params=[
            {
                "to": token_contract_address,
                "data": "0x" + call_data.hex(),
            },
            "latest",
        ],
    )
    return result_hex


def get_erc20_decimals(token_contract_address: str) -> int:
    # decimals() tells wallets how many decimal places to show for this token.
    # USDC uses 6, while many other ERC-20 tokens use 18.
    decimals_selector = keccak256(data=b"decimals()")[:4]
    result_hex = call_erc20(
        token_contract_address=token_contract_address,
        function_selector=decimals_selector,
        function_arguments=[],
    )
    decimals = int(result_hex, 16)
    return decimals


def encode_erc20_transfer_data(
    recipient_address: str,
    token_amount: int,
) -> bytes:
    # ERC-20 transfer(address,uint256) moves token units from the transaction
    # signer to the recipient. The ETH value of the transaction will be 0.
    transfer_selector = keccak256(data=b"transfer(address,uint256)")[:4]
    encoded_recipient_address = (
        b"\x00" * 12 + bytes.fromhex(recipient_address.removeprefix("0x"))
    )
    encoded_token_amount = token_amount.to_bytes(32, "big")
    transfer_data = transfer_selector + encoded_recipient_address + encoded_token_amount
    return transfer_data

def get_erc20_string(token_contract_address: str, selector: bytes) -> str:
    result_hex = call_erc20(
        token_contract_address=token_contract_address,
        function_selector=selector,
        function_arguments=[],
    )
    text = decode_abi_string(result_hex=result_hex)
    return text


def get_erc20_balance(token_contract_address: str, wallet_address: str) -> int:
    # ERC-20 tokens are smart contracts. balanceOf(address) is a read-only
    # contract call that returns how many token units an address owns.
    balanceOf_address_selector = keccak256(data=b"balanceOf(address)")[:4]

    wallet_address_bytes = bytes.fromhex(wallet_address.removeprefix("0x"))
    # Ethereum ABI arguments are 32 bytes each. An address is 20 bytes, so it is
    # left-padded with 12 zero bytes.
    encoded_wallet_address = b"\x00" * 12 + wallet_address_bytes

    erc20_balance_hex = call_erc20(
        token_contract_address=token_contract_address,
        function_selector=balanceOf_address_selector,
        function_arguments=[encoded_wallet_address],
    )
    erc20_balance = int(erc20_balance_hex, 16)
    return erc20_balance
