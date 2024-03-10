import os
import random
from typing import Iterable
from string import ascii_letters, digits


def generate_user_keys(key_length: int, n: int) -> list[str]:
    """Generates random `n` user keys of length `key_length`"""
    return [os.urandom(key_length).hex().upper() for _ in range(n)]

def insert_user_keys(filepath: str, user_keys: Iterable[str]) -> None:
    """Inserts user keys into a file"""
    _, file_extension = os.path.splitext(filepath)

    assert os.path.exists(filepath)
    assert file_extension == ".csv"

    with open(filepath, "w+") as f:
        f.writelines([key.split("\n")[0] + "\n" for key in user_keys])
