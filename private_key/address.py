import os
import sys

from coincurve import PrivateKey

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from create import PRIVATE_KEY_PATH
from internal.utilities import keccak256

ADDRESS_PATH = 'address.txt'

if __name__ == "__main__":
    with open(PRIVATE_KEY_PATH) as f:
        private_key_hex = f.read()
    private_key_bytes = bytes.fromhex(private_key_hex.removeprefix("0x"))
    private_key = PrivateKey(private_key_bytes)

    # coincurve returns an uncompressed public key as 65 bytes:
    # 1 prefix byte 0x04, then 32 bytes x and 32 bytes y.
    public_key_bytes = private_key.public_key.format(compressed=False)[1:]

    # Hash the public key and keep the last 20 bytes. Those 20 bytes are the
    # raw Ethereum address.
    address_bytes = keccak256(data=public_key_bytes)[-20:]

    address_hex = "0x" + address_bytes.hex()
    with open(ADDRESS_PATH, "w") as address_file:
        address_file.write(address_hex)
