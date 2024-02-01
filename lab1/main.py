from itertools import cycle
from string import ascii_letters
from typing import Iterator

from tqdm import tqdm


TEST_FILE_PATH: str = "/Users/mishashkarubski/PycharmProjects/NetworkSecurity/lab1/test.txt"


class FileEncryptor:
    ALPH: str = ascii_letters + "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

    def __init__(self, file: str, mode: str, cipher, key: int | str):
        self.file = file
        self.mode = mode
        self.cipher = cipher
        self.key = key

        assert ((cipher == 'caesar' and isinstance(key, int)) or
                (cipher == 'vigenere' and isinstance(key, str)))

        if cipher == 'vigenere':
            n_letters = len(self.ALPH)
            self.letter_matrix = []

            for i in range(n_letters):
                self.letter_matrix += [list(self.ALPH[i % n_letters:] + self.ALPH[:i % n_letters])]

    def _encrypt_caesar(self, text: str, reverse=False):
        encrypted: str = ""

        for c in tqdm(text, desc="Encrypting" if not reverse else "Decrypting"):
            if c in self.ALPH:
                c_ind = self.ALPH.index(c)

                if not reverse:
                    encrypted += self.ALPH[(c_ind + self.key) % len(self.ALPH)]
                else:
                    encrypted += self.ALPH[(c_ind - self.key + len(self.ALPH)) % len(self.ALPH)]

            else:
                encrypted += c

        return encrypted

    def _encrypt_vigenere(self, text: str, reverse=False):
        encrypted: str = ""
        key: str = ""

        for k in cycle(self.key):
            key += k
            if len(key) == len(list(filter(lambda x: x in self.ALPH, text))):
                break

        key_iterator: Iterator = iter(key)

        for c in tqdm(text, desc="Encrypting" if not reverse else "Decrypting"):
            if c in self.ALPH and not reverse:
                k_ind: int = self.ALPH.index(next(key_iterator))
                c_ind: int = self.ALPH.index(c)
                encrypted += self.letter_matrix[k_ind][c_ind]
            elif c in self.ALPH and reverse:
                k_ind: int = self.ALPH.index(next(key_iterator))
                c_ind: int = self.letter_matrix[k_ind].index(c)
                encrypted += self.ALPH[c_ind]
            else:
                encrypted += c

        return encrypted

    def encrypt(self, text: str, reverse=False) -> str:
        encrypted = ""

        if self.cipher == 'caesar':
            encrypted = self._encrypt_caesar(text, reverse=reverse)
        elif self.cipher == 'vigenere':
            encrypted = self._encrypt_vigenere(text, reverse=reverse)

        return encrypted

    def __enter__(self):
        assert (self.mode in ["r", "w", "r+", "w+"])

        self._f = open(self.file, self.mode, encoding='utf-8')

        return self._f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._f.close()


if __name__ == "__main__":
    file_enc = FileEncryptor(TEST_FILE_PATH, 'r', 'vigenere', 'amogstvo')

    with file_enc as fe:
        data = fe.read()

    encr = file_enc.encrypt(data, reverse=False)
    decr = file_enc.encrypt(encr, reverse=True)

    print(encr)
    print(decr)
