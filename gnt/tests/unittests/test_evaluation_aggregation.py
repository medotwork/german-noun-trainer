from itertools import groupby
from typing import List
import numpy as np

class Evaluation:

    def __init__(self, key:str, recorded_results: list,
                 mean_result: np.float64, count_results: int):
        self.key = key
        self.recorded_results = recorded_results
        self.mean_result = mean_result
        self.count_results = count_results

    @staticmethod
    def from_tuple_list(tl):
        return [Evaluation(*t) for t in tl]

    def __eq__(self, other):
        return (self.key==other.key) and \
                (self.recorded_results==other.recorded_results) and \
                (self.mean_result==other.mean_result) and \
                (self.count_results== other.count_results)

    @staticmethod
    def eval_aggregation(combined_eval):
        def key_fun(t:tuple):
            return t[0]

        sorted_eval = sorted(combined_eval, key=key_fun)

        grouped_eval = groupby(sorted_eval, key=key_fun)
        aggregated_eval = []

        for i, g in grouped_eval:
            aggregated_eval.append((i, [j[1] for j in list(g)]))

        return [Evaluation(i[0], i[1], np.mean(i[1]), len(i[1])) for i in aggregated_eval]

def test_aggregation():
    evaluation = [("1", 0), ("0", 0), ("1", 1), ("1", 1), ("1", 1)]
    assert Evaluation.eval_aggregation(evaluation) == Evaluation.from_tuple_list([
            ("0", [0], np.float64(0), 1),
            ("1", [0, 1, 1, 1], np.float64(0.75), 4),
            ])


def test_combine_evaluations():
    evaluation_a = [("1", 0), ("1", 1), ("0", 0), ("0", 0)]
    evaluation_b = [("2", 0), ("1", 1), ("0", 0), ("0", 0)]
    evaluation_c = [("3", 0), ("1", 1), ("0", 0), ("0", 0)]

    combined_evals = []
    for i in [evaluation_a, evaluation_b, evaluation_c]:
        combined_evals += i

    assert combined_evals == [("1", 0), ("1", 1), ("0", 0), ("0", 0),
                              ("2", 0), ("1", 1), ("0", 0), ("0", 0),
                              ("3", 0), ("1", 1), ("0", 0), ("0", 0)]

def test_filter_percentage():
    def filter_percentage(evals: list, indexes: list = None,
                          percentage_value = 0.75, under = True):
        def filter_fun(item):
            if under:
                return item if item < percentage_value else None
            else:
                return item if item >=percentage_value else None
        

        filtered = [i.key for i in evals if filter_fun(i.mean_result)] 

        if indexes and under:
            return sorted(list(set(filtered + [i for i in indexes if i not in [j.key for j in evals]])))
        else:
            return filtered

    data_file_indexes = ["0", "1", "2", "3", "4"]
    combined_evals = [
            ("0", 0), ("0", 0), ("0", 1), # 33%
            ("1", 0), ("1", 0), ("1", 1), ("1", 1), # 50%
            ("2", 0), ("2", 1), ("2", 1), ("2", 1), # 75%
            ("3", 0), ("3", 1), ("3", 1), ("3", 1), ("3", 1), # 80%
            ]

    aggregation = Evaluation.eval_aggregation(combined_evals)

    assert filter_percentage(evals=aggregation, indexes=data_file_indexes) == ["0", "1", "4"]
    assert filter_percentage(evals=aggregation) == ["0", "1"]
    assert filter_percentage(evals=aggregation, percentage_value=0.75, under=False) == ["2", "3"]
    assert filter_percentage(evals=aggregation, percentage_value=0.76, under=False) == ["3"]
