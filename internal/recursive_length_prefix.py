def encode_bytes(value: bytes) -> bytes:
    # RLP encodes one byte below 0x80 as itself. This keeps very small values
    # compact, such as the empty transaction type prefix or tiny integers after
    # they have been converted to bytes.
    if len(value) == 1 and value[0] < 0x80:
        return value

    # For byte strings from 0 to 55 bytes, RLP stores one prefix byte followed
    # by the bytes themselves. The prefix is 0x80 plus the length.
    if len(value) <= 55:
        return bytes([0x80 + len(value)]) + value

    # Longer byte strings store the length of the length first. We do not need
    # this for most simple transaction fields, but it is part of RLP.
    length_bytes = len(value).to_bytes((len(value).bit_length() + 7) // 8, "big")
    return bytes([0xB7 + len(length_bytes)]) + length_bytes + value


def encode_integer(value: int) -> bytes:
    # RLP has no special integer type. Integers are converted to their shortest
    # big-endian byte form, then encoded as bytes.
    if value == 0:
        return encode_bytes(b"")

    value_bytes = value.to_bytes((value.bit_length() + 7) // 8, "big")
    return encode_bytes(value_bytes)


def encode_list(values: list) -> bytes:
    # Lists are encoded by first encoding every item, then prefixing the total
    # encoded payload length.
    payload = b""
    for value in values:
        payload += encode(value)

    if len(payload) <= 55:
        return bytes([0xC0 + len(payload)]) + payload

    length_bytes = len(payload).to_bytes((len(payload).bit_length() + 7) // 8, "big")
    return bytes([0xF7 + len(length_bytes)]) + length_bytes + payload


def encode(value) -> bytes:
    if isinstance(value, bytes):
        return encode_bytes(value)

    if isinstance(value, int):
        return encode_integer(value)

    if isinstance(value, list):
        return encode_list(value)

    raise TypeError(f"Cannot RLP encode {type(value)}")
