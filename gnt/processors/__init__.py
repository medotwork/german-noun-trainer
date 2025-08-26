import os
import glob
import numpy as np

from pathlib import Path
from datetime import datetime, timedelta

class FileHandler:
    @staticmethod
    def find_records_path(data_file: str):
        record_folder = Path(__file__).parent.parent / "records" / data_file
        return record_folder
    
    @staticmethod
    def find_records(data_file: str):
        return FileHandler.find_records_path(data_file).glob('*.log')

class Filter:
    def __init__(self):
        self.instdatetime = datetime.now()

    def filter_by_mode(self, indexes: list, data_file:str, mode: str):
        out = indexes
        if mode != "n":
            files = [(datetime.strptime(p.stem).date(), p) for p in FileHandler.find_records(data_file)]
            seven_day_files = [f for f in files if f[0] >= (self.instdatetime.date()-timedelta(days=7))]
            evaluation = [(f[0], f[1], Evaluator.day_metrics(f[1])) for f in seven_day_files]

        if mode == "improve_75":
            out = []
        elif mode == "maintain_75":
            out = []
        
        return out if out else indexes
        
class Evaluator:
    @staticmethod
    def aggregate_evaluations(l: list):
        pass

    @staticmethod
    def day_metrics(day_record_path: Path):

        with open(day_record_path, 'r', encoding='utf8') as f:
            lines = f.readlines()

        day_list = [l.strip().split('\t') for l in lines]
        day_previous_item_list = [(None, None)] + day_list

        day_list += [(None, None)]
        
        return [(i[0],0.0) if i[0]==j[0] and j[1]==0 else (0,1.0) for i, j in zip(day_list, day_previous_item_list) if i[1]]
#        return [(i[0], 0.0) if (i[0]==j[0] and j[1]==0) else (i[0], 1.0) for i, j in zip(day_list, day_previous_item_list) if i[1]]

    @staticmethod
    def evaluate(data_file: str, mode: str = 'daily'):
        daily_records_folder = FileHandler.find_records(data_file)

        word_results = [(f.stem, Evaluator.day_metrics(f)) for f in daily_records_folder]

        out = []

        for result in word_results:
            out.append(
                    (datetime.strptime(result[0], '%Y-%m-%d').date(),
                round(np.mean([i[1] for i in result[1]])*100, 2))
                    )

        return out
