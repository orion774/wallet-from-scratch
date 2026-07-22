import argparse

from internal.erc20 import (
    get_erc20_balance,
    get_erc20_decimals,
    get_erc20_string,
    TOKEN_SYMBOL_TO_CONTRACT_ADDRESS,
)
from internal.utilities import ADDRESS_PATH, keccak256

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token-symbol", default="USDC")
    args = parser.parse_args()

    token_contract_address = TOKEN_SYMBOL_TO_CONTRACT_ADDRESS[args.token_symbol]

    with open(ADDRESS_PATH) as f:
        wallet_address = f.read().strip()
    name = get_erc20_string(
        token_contract_address=token_contract_address,
        selector=keccak256(data=b"name()")[:4],
    )
    symbol = get_erc20_string(
        token_contract_address=token_contract_address,
        selector=keccak256(data=b"symbol()")[:4],
    )
    decimals = get_erc20_decimals(token_contract_address=token_contract_address)
    token_balance = get_erc20_balance(
        token_contract_address=token_contract_address,
        wallet_address=wallet_address,
    )
    token_amount = token_balance / 10**decimals

    print(f"Address:  {wallet_address}")
    print(f"Token:    {name}")
    print(f"Amount:   {token_amount} {symbol}")
