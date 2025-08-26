import numpy as np
from processors import FileHandler, Evaluator

def test_FileHandler():
    files = FileHandler.find_records('test_words')
    assert len([i for i in files]) == 1

def test_Evaluator_evaluation():
    evaluation = Evaluator.day_metrics('./records/test_words/2000-08-28.log')
    expected_evaluation = [(0, 0.0), (1,1.0), (0,1.0), (2, 0.0)]
    assert len(expected_evaluation) == len(evaluation)
    assert expected_evaluation == evaluation
    assert np.mean([i[1] for i in evaluation]) == 0.5 
