import os
from hashlib import blake2b
from typing import Text


def encode_string(s: Text, size: int = 10) -> Text:
    """
    Function hashes provided string by BLAKE2 cryptographic algorithm
    https://docs.python.org/3/library/hashlib.html#blake2
    :param s: string to encode
    :param size: integer with size of encoded hash
    :return: hashed string with length equal to size parameter
    """

    if not isinstance(size, int):
        raise TypeError('size parameter should be an integer')
    if not s or size <= 0 or size > 128:
        raise ValueError('s parameter should not be empty and should be between 1 - 128')
    salt = os.urandom(blake2b.SALT_SIZE)
    return blake2b(bytes(str(s), encoding='utf-8'), salt=salt).hexdigest()[:size]
