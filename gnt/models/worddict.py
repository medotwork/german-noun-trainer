from pathlib import Path
from random import sample
from typing import List
from models.article import DeArtikels


DEFAULT_DATA_FILE_NAME = "most_common_nouns.csv"
DEFAULT_DATA_FILE_PATH = Path(__file__).parent.parent / "data"

class WordDictEntry:
    def __init__(self, word_en, word_de, word_de_artikel):
        self.word_en = word_en
        self.word_de = word_de,
        self.word_de_artikel = DeArtikels.from_key(word_de_artikel)
        if self.word_de_artikel is None:
            raise Exception(f'No valid article found for {word_en} {word_de} {word_de_artikel}')

class WordDict:
    def __init__(self, entries: List[WordDictEntry]):
        self.entries = entries
    
    @staticmethod
    def from_default_csv(path: Path= DEFAULT_DATA_FILE_PATH  / DEFAULT_DATA_FILE_NAME):
        if not Path.exists(path):
            raise Exception(f"Could not find word dict data: {str(path.absolute())}")

        with open(path, 'r', encoding='utf8') as default_csv:
            word_data = default_csv.readlines()

        words_dict = {index: item.strip().split('\t') for index, item in enumerate(word_data)}

        entries: List[WordDictEntry] = [] 
        for k, v in words_dict.items():
            try:
                entries.append(
                     WordDictEntry(
                         word_en = v[0].split(' ')[1],
                         word_de = v[1].split(' ')[1] if ' ' in v[1] else '',
                         word_de_artikel = v[1].split(' ')[0].lower() if ' ' in v[1] else v[1],
                         )
                     )
            except:
                pass
        return WordDict(entries = entries) 

    def select_word(self) -> (int, WordDictEntry):
        selected_index = sample(range(0, len(self.entries)), 1)[0]
        return selected_index, self.entries[selected_index]

    def verify_index(self, selected_index: int, artikel: DeArtikels) -> bool:
        return True if self.entries[selected_index].word_de_artikel == artikel else False

