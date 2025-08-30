from dataclasses import dataclass
from enum import Enum

@dataclass
class Artikel:
    lowercase: str
    classes_key: str
    keyboard_key: str

class DeArtikels(Artikel, Enum):
    DER = 'der', 'der_label', 'i'
    DIE = 'die', 'die_label', 'o'
    DAS = 'das', 'das_label', 'p'

    def __eq__(a, b):
        return a.lowercase == b.lowercase

    @classmethod
    def from_lowercase(cls, lowercase: str):
        return next((artikel for artikel in (cls.DER, cls.DIE, cls.DAS) if artikel.lowercase == lowercase), None)

    @classmethod
    def from_key(cls, key: str):
        return next((artikel for artikel in (cls.DER, cls.DIE, cls.DAS) if artikel.keyboard_key == key), None)

    @classmethod
    def keys(cls):
        return ['i','o','p']
