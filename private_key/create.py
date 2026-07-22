import os

from coincurve import PrivateKey

PRIVATE_KEY_PATH = "private_key/private_key.txt"

if __name__ == "__main__":
    private_key = PrivateKey()
    private_key_hex = "0x" + private_key.secret.hex()

    assert not os.path.exists(PRIVATE_KEY_PATH)
    with open(PRIVATE_KEY_PATH, "w") as private_key_file:
        private_key_file.write(private_key_hex)

    print(f"Created {PRIVATE_KEY_PATH}")
