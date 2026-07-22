import argparse

from internal.remote_procedure_call import get_transaction_receipt
from internal.utilities import WEI_PER_ETH, GWEI

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transaction-hash", required=True)
    args = parser.parse_args()

    receipt = get_transaction_receipt(args.transaction_hash)
    if receipt is None:
        print("Transaction is still pending.")
    else:
        status = int(receipt["status"], 16)
        block_number = int(receipt["blockNumber"], 16)
        gas_used = int(receipt["gasUsed"], 16)
        effective_gas_price = int(receipt["effectiveGasPrice"], 16)
        fee_wei = gas_used * effective_gas_price
        fee_eth = fee_wei / WEI_PER_ETH

        print(f"Transaction:         {args.transaction_hash}")
        print(f"Status:              {status}")
        print(f"Block number:        {block_number}")
        print(f"Gas used:            {gas_used}")
        print(f"Effective gas price: {effective_gas_price / GWEI} gwei")
        print(f"Fee ETH:             {fee_eth}")
