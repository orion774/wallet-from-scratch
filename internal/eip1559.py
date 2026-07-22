import json
import subprocess
import sys

from internal.recursive_length_prefix import encode
from internal.remote_procedure_call import rpc_call
from internal.utilities import SIGNER_PATH, keccak256


def sign_and_broadcast_transaction(
    transaction_type: bytes,
    chain_id: int,
    signer_nonce: int,
    max_priority_fee_per_gas: int,
    max_fee_per_gas: int,
    gas_limit: int,
    destination: str,
    amount: int,
    payload: bytes,
    access_list: list,
) -> str:
    unsigned_transaction = [
        chain_id,
        signer_nonce,
        max_priority_fee_per_gas,
        max_fee_per_gas,
        gas_limit,
        bytes.fromhex(destination.removeprefix("0x")),  # bytes
        amount,
        payload,  # bytes
        access_list,
    ]

    bytes_to_sign = transaction_type + encode(unsigned_transaction)
    bytes_hash = keccak256(data=bytes_to_sign)

    # This is the signing boundary. It asks the private-key module to sign a
    # 32-byte hash and returns the Ethereum signature fields.
    signature_json = subprocess.check_output(
        [
            sys.executable,
            SIGNER_PATH,
            "0x" + bytes_hash.hex(),
        ],
        text=True,
    )
    signature = json.loads(signature_json)
    transaction_signature = [
        signature["y_parity"],
        int(signature["r"], 16),
        int(signature["s"], 16),
    ]

    transaction_with_signature = unsigned_transaction + transaction_signature
    transaction_with_signature_bytes = encode(transaction_with_signature)
    typed_transaction_with_signature_bytes = (
        transaction_type + transaction_with_signature_bytes
    )
    typed_transaction_with_signature_hex = "0x" + typed_transaction_with_signature_bytes.hex()

    transaction_hash = rpc_call(
        method="eth_sendRawTransaction",
        params=[typed_transaction_with_signature_hex],
    )
    return transaction_hash


def get_fees() -> tuple[int, int, int]:
    # EIP-1559 blocks include a baseFeePerGas value. This is the minimum fee
    # per gas that a transaction must pay for the block.
    block = rpc_call(
        method="eth_getBlockByNumber",
        params=["latest", False],
    )
    base_fee_per_gas = int(block["baseFeePerGas"], 16)

    # The priority fee is the tip paid to the block builder/validator.
    priority_fee_hex = rpc_call(
        method="eth_maxPriorityFeePerGas",
        params=[],
    )
    priority_fee_per_gas = int(priority_fee_hex, 16)
    max_fee_per_gas = base_fee_per_gas * 2 + priority_fee_per_gas

    return base_fee_per_gas, priority_fee_per_gas, max_fee_per_gas
