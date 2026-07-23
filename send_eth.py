import argparse

from internal.eip1559 import sign_and_broadcast_transaction, get_fees
from internal.remote_procedure_call import rpc_call
from internal.utilities import ADDRESS_PATH, WEI_PER_ETH, GWEI


CHAIN_ID = 11155111 # Sepolia testnet
GAS_LIMIT = 21000
TRANSACTION_TYPE = b"\x02"


if __name__ == "__main__":
    # This script sends real ETH on Ethereum mainnet. Use an address you control.
    parser = argparse.ArgumentParser()
    parser.add_argument("--to-address", required=True)
    parser.add_argument("--send-value-wei", type=int, default=10**14)
    args = parser.parse_args()

    with open(ADDRESS_PATH) as f:
        from_address = f.read().strip()

    # eth_getTransactionCount returns the number of transactions sent from an
    # address. Ethereum uses this number as the nonce for the next transaction.
    nonce_hex = rpc_call(
        method="eth_getTransactionCount",
        params=[from_address, "latest"],
    )
    nonce = int(nonce_hex, 16)

    base_fee_per_gas, priority_fee_per_gas, max_fee_per_gas = get_fees()
    estimated_transaction_fee_wei = GAS_LIMIT * (base_fee_per_gas + priority_fee_per_gas)
    maximum_transaction_fee_wei = GAS_LIMIT * max_fee_per_gas

    print("About to send ETH on Ethereum mainnet.")
    print(f"From:             {from_address}")
    print(f"To:               {args.to_address}")
    print(f"Value:            {args.send_value_wei / WEI_PER_ETH} ETH")
    print(f"Estimated fee:    {estimated_transaction_fee_wei / WEI_PER_ETH} ETH")
    print(f"Max fee:          {maximum_transaction_fee_wei / WEI_PER_ETH} ETH")
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
        gas_limit=GAS_LIMIT,
        destination=args.to_address,
        amount=args.send_value_wei,
        payload=b"",
        access_list=[],
    )
    print(f"Transaction hash: {transaction_hash}")
