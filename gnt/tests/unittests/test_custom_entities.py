from enum import Enum
from dataclasses import dataclass
from models.worddict import WordDict, WordDictEntry 
from models.article import DeArtikels
import unittest

class TestDeArtikel(unittest.TestCase):
    def test_from_key(self):
        self.assertTrue(DeArtikels.DER.lowercase=='der')
        self.assertTrue(DeArtikels.from_key('der').lowercase == 'der')
        self.assertTrue(DeArtikels.from_key('das').lowercase == 'das')
        self.assertTrue(DeArtikels.from_key('die').lowercase == 'die')
        self.assertFalse(DeArtikels.from_key('die').lowercase == 'das')
        self.assertIsNone(DeArtikels.from_key('DIE'))

    def test_eq(self):
        self.assertTrue(DeArtikels.from_key('die') == DeArtikels.DIE)
        self.assertFalse(DeArtikels.from_key('die') == DeArtikels.DER)

class TestWordDictEntry(unittest.TestCase):
    def test_init(self):
        entries_input = [
            ('word', 'Wort', 'die'),
            ('word', 'Wort', 'DIE')
                ]
        self.assertTrue(WordDictEntry(*entries_input[0]))
        self.assertTrue(WordDictEntry(*entries_input[0]).word_de_artikel.lowercase == 'die')
        self.assertFalse(WordDictEntry(*entries_input[0]).word_de_artikel.lowercase == 'der')
        self.assertRaises(Exception, WordDictEntry, *entries_input[1])

class TestWordDict(unittest.TestCase):
    def test_default_csv(self):
        word_dict = WordDict.from_default_csv()
        self.assertTrue(len(word_dict.entries) > 10)

    def test_select_word(self):
        word_dict = WordDict.from_default_csv()
        selected_index, selected_word = word_dict.select_word()
        self.assertIsInstance(selected_word, WordDictEntry)
        
    def test_verify(self):
        artikel_options = [
            DeArtikels.DER,
            DeArtikels.DIE,
            DeArtikels.DAS,
                ]
        word_dict = WordDict.from_default_csv()
        selected_index, selected_word = word_dict.select_word()
       
        selected_word_key = selected_word.word_de_artikel.lowercase

        self.assertTrue(word_dict.verify_index(selected_index, DeArtikels.from_key(selected_word_key)))

        artikel_options.pop(artikel_options.index(selected_word.word_de_artikel))

        self.assertFalse(word_dict.verify_index(selected_index, artikel_options[0]))


if __name__ == '__main__':
    unittest.main()

