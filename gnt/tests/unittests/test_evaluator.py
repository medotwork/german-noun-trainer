import numpy as np
from processors import FileHandler, Evaluator
import unittest
import logging

class TestDeArtikel(unittest.TestCase):
    def test_FileHandler(self):
        files = FileHandler.find_records('test_words')
        self.assertTrue(len([i for i in files]) == 2)

    def test_Evaluator_day_metrics(self):
        evaluation = Evaluator.day_metrics('./records/test_words/2000-08-28.log')
        expected_evaluation = [(0, 0.0), (1,1.0), (0,1.0), (2, 0.0)]
        self.assertTrue(len(expected_evaluation) == len(evaluation))
        self.assertTrue(expected_evaluation == evaluation)
        self.assertTrue(np.mean([i[1] for i in evaluation]) == 0.5) 
    
    def test_Evaluator_evaluate(self):
        logging.error('a')

if __name__ == '__main__':
    unittest.main()

