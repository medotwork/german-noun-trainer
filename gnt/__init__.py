import os
from pathlib import Path
from random import sample

DATA_FILE_NAME = "most_common_nouns.csv"
SET_SIZE = 10

with open(Path(__file__).parent / "data" / DATA_FILE_NAME, 'r') as f:
    data = f.readlines()

words_dict = {index: item.strip().split('\t') for index, item in enumerate(data)}

for k, v in words_dict.items():
    words_dict[k] = {
            'en': v[0].split(' ')[1],
            'de artikel': v[1].split(' ')[0].lower() if ' ' in v[1] else v[1],
            'de': v[1].split(' ')[1] if ' ' in v[1] else '',
            }

set_idx = sample(range(0,2000), SET_SIZE)
print([words_dict[i] for i in set_idx])
