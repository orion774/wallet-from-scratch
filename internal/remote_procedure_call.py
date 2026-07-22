import requests

# Free public Ethereum mainnet JSON-RPC endpoint.
# Public RPCs are fine for learning, but they can be rate-limited or unavailable.
RPC_URL = "https://ethereum-rpc.publicnode.com"
# Backups:
# https://eth.llamarpc.com
# https://1rpc.io/eth
# https://public-eth.nownodes.io


def rpc_call(method: str, params: list):
    """Call an Ethereum JSON-RPC method and return its result."""
    body = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }

    response = requests.post(RPC_URL, json=body)
    response_json = response.json()
    assert "error" not in response_json

    return response_json["result"]


def get_balance_wei(address: str) -> int:
    # eth_getBalance returns the balance as hex wei.
    balance_hex = rpc_call("eth_getBalance", [address, "latest"])
    balance_wei = int(balance_hex, 16)
    return balance_wei


def estimate_gas(
    from_address: str,
    to_address: str,
    value: int,
    data: bytes,
) -> int:
    gas_hex = rpc_call(
        method="eth_estimateGas",
        params=[
            {
                "from": from_address,
                "to": to_address,
                "value": hex(value),
                "data": "0x" + data.hex(),
            }
        ],
    )
    gas = int(gas_hex, 16)
    return gas
    

def get_transaction_receipt(transaction_hash: str):
    # A transaction receipt exists after a transaction has been included in a
    # block. If the transaction is still pending, the result is null.
    receipt = rpc_call("eth_getTransactionReceipt", [transaction_hash])
    return receipt
    
