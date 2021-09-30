from string import ascii_lowercase
from typing import Dict


class Cipher:
    def __init__(self, keyword: str):
        self._cipher = keyword.lower() + "".join(char for char in ascii_lowercase if char not in keyword.lower())
        self._encode_correlations = dict(zip(ascii_lowercase, self._cipher))
        self._decode_correlations = dict(zip(self._cipher, ascii_lowercase))

    def encode(self, string: str) -> str:
        return self._encryptor(string, self._encode_correlations)

    def decode(self, string: str) -> str:
        return self._encryptor(string, self._decode_correlations)

    @staticmethod
    def _encryptor(string: str, correlations: Dict[str, str]) -> str:
        result = ""
        for char in string:
            result_char = correlations.get(char.lower(), char)
            result += result_char.upper() if char.isupper() else result_char

        return result


if __name__ == "__main__":
    cipher = Cipher("crypto")
    print(cipher.encode("Hello world"))
    print(cipher.decode("Fjedhc dn atidsn"))
