import json
import sys

from coincurve import PrivateKey

from create import PRIVATE_KEY_PATH

if __name__ == "__main__":
    payload_hash_hex = sys.argv[1]
    payload_hash = bytes.fromhex(payload_hash_hex.removeprefix("0x"))
    assert len(payload_hash) == 32

    with open(PRIVATE_KEY_PATH) as f:
        private_key_hex = f.read()

    private_key_bytes = bytes.fromhex(private_key_hex.removeprefix("0x"))
    private_key = PrivateKey(private_key_bytes)

    recoverable_signature = private_key.sign_recoverable(payload_hash, hasher=None)

    signature_r = int.from_bytes(recoverable_signature[0:32], "big")
    signature_s = int.from_bytes(recoverable_signature[32:64], "big")
    signature_y_parity = recoverable_signature[64] % 2

    print(
        json.dumps(
            {
                "y_parity": signature_y_parity,
                "r": "0x" + signature_r.to_bytes(32, "big").hex(),
                "s": "0x" + signature_s.to_bytes(32, "big").hex(),
            }
        )
    )
