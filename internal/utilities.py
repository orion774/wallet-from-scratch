import requests
from Crypto.Hash import keccak

ADDRESS_PATH = "address.txt"
PRIVATE_KEY_PATH = "private_key/private_key.txt"
SIGNER_PATH = "private_key/sign.py"

WEI_PER_ETH = 10**18
GWEI = 10**9

def keccak256(data: bytes) -> bytes:
    """Return Ethereum's Keccak-256 hash for some bytes."""
    digest = keccak.new(digest_bits=256)
    digest.update(data)
    return digest.digest()


def decode_abi_string(result_hex: str) -> str:
    result_bytes = bytes.fromhex(result_hex.removeprefix("0x"))
    string_offset = int.from_bytes(result_bytes[0:32], "big")
    string_length = int.from_bytes(
        result_bytes[string_offset : string_offset + 32],
        "big",
    )
    string_start = string_offset + 32
    string_end = string_start + string_length
    text = result_bytes[string_start:string_end].decode("utf-8")
    return text