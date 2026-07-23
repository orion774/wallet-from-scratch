import argparse

from internal.eip1559 import sign_and_broadcast_transaction, get_fees
from internal.erc20 import (
    encode_erc20_transfer_data,
    get_erc20_decimals,
    TOKEN_SYMBOL_TO_CONTRACT_ADDRESS
)
from internal.remote_procedure_call import rpc_call, estimate_gas
from internal.utilities import ADDRESS_PATH, WEI_PER_ETH, GWEI
from send_eth import CHAIN_ID, TRANSACTION_TYPE


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token-symbol", default="TestUSDC")
    parser.add_argument("--to-address", required=True)
    parser.add_argument("--send-value", type=int, default=1)
    args = parser.parse_args()

    token_contract_address = TOKEN_SYMBOL_TO_CONTRACT_ADDRESS[args.token_symbol]
    with open(ADDRESS_PATH) as f:
        from_address = f.read().strip()

    # eth_getTransactionCount returns the number of transactions sent from an
    # address. Ethereum uses this number as the nonce for the next transaction.
    nonce_hex = rpc_call(
        method="eth_getTransactionCount",
        params=[from_address, "latest"],
    )
    nonce = int(nonce_hex, 16)

    transfer_data = encode_erc20_transfer_data(
        recipient_address=args.to_address,
        token_amount=args.send_value,
    )

    gas_limit = estimate_gas(
        from_address=from_address,
        to_address=token_contract_address,
        value=0,
        data=transfer_data,
    )
    base_fee_per_gas, priority_fee_per_gas, max_fee_per_gas = get_fees()
    estimated_fee_wei = gas_limit * (base_fee_per_gas + priority_fee_per_gas)
    maximum_fee_wei = gas_limit * max_fee_per_gas

    decimals = get_erc20_decimals(token_contract_address=token_contract_address)
    token_amount = args.send_value / 10**decimals
    print("About to send ERC-20 tokens on Ethereum mainnet.")
    print(f"From:             {from_address}")
    print(f"Token contract:   {token_contract_address}")
    print(f"Recipient:        {args.to_address}")
    print(f"Token amount:     {token_amount} {args.token_symbol}")
    print(f"Estimated fee:    {estimated_fee_wei / WEI_PER_ETH} ETH")
    print(f"Max fee:          {maximum_fee_wei / WEI_PER_ETH} ETH")
    confirmation = input("Type 'send' to sign and broadcast this transaction: ")
    if confirmation != "send":
        print("Transaction cancelled.")
        raise SystemExit

    transaction_hash = sign_and_broadcast_transaction(
        transaction_type=TRANSACTION_TYPE,
        chain_id=CHAIN_ID,
        signer_nonce=nonce,
        max_priority_fee_per_gas=priority_fee_per_gas,
        max_fee_per_gas=max_fee_per_gas,
        gas_limit=gas_limit,
        destination=token_contract_address,
        amount=0,  # ETH value to send in wei
        payload=transfer_data,
        access_list=[],
    )
    print(f"Transaction hash: {transaction_hash}")
